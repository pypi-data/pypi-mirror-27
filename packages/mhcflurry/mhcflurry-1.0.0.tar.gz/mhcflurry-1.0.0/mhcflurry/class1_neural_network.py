import time
import collections
import logging

import numpy
import pandas

from mhcflurry.hyperparameters import HyperparameterDefaults

from mhcflurry.encodable_sequences import EncodableSequences
from mhcflurry.amino_acid import available_vector_encodings, vector_encoding_length
from mhcflurry.regression_target import to_ic50, from_ic50
from mhcflurry.common import random_peptides, amino_acid_distribution


class Class1NeuralNetwork(object):
    """
    Low level class I predictor consisting of a single neural network.
    
    Both single allele and pan-allele prediction are supported, but pan-allele
    is in development and not yet well performing.
    
    Users will generally use Class1AffinityPredictor, which gives a higher-level
    interface and supports ensembles.
    """

    network_hyperparameter_defaults = HyperparameterDefaults(
        kmer_size=15,
        use_embedding=False,
        peptide_amino_acid_encoding="one-hot",
        embedding_input_dim=21,
        embedding_output_dim=8,
        pseudosequence_use_embedding=False,
        layer_sizes=[32],
        dense_layer_l1_regularization=0.001,
        dense_layer_l2_regularization=0.0,
        activation="relu",
        init="glorot_uniform",
        output_activation="sigmoid",
        dropout_probability=0.0,
        batch_normalization=False,
        embedding_init_method="glorot_uniform",
        locally_connected_layers=[
            {
                "filters": 8,
                "activation": "tanh",
                "kernel_size": 3
            }
        ],
    )
    """
    Hyperparameters (and their default values) that affect the neural network
    architecture.
    """

    compile_hyperparameter_defaults = HyperparameterDefaults(
        loss="mse",
        optimizer="rmsprop",
    )
    """
    Loss and optimizer hyperparameters. Any values supported by keras may be
    used.
    """

    input_encoding_hyperparameter_defaults = HyperparameterDefaults(
        left_edge=4,
        right_edge=4)
    """
    Number of amino acid residues that are given fixed positions on the each
    side in the variable length encoding.
    """

    fit_hyperparameter_defaults = HyperparameterDefaults(
        max_epochs=500,
        take_best_epoch=False,  # currently unused
        validation_split=0.2,
        early_stopping=True,
        minibatch_size=128,
        random_negative_rate=0.0,
        random_negative_constant=25,
        random_negative_affinity_min=20000.0,
        random_negative_affinity_max=50000.0,
        random_negative_match_distribution=True,
        random_negative_distribution_smoothing=0.0)
    """
    Hyperparameters for neural network training.
    """

    early_stopping_hyperparameter_defaults = HyperparameterDefaults(
        patience=10,
        monitor='val_loss',  # currently unused
        min_delta=0,  # currently unused
        verbose=1,  # currently unused
        mode='auto'  # currently unused
    )
    """
    Hyperparameters for early stopping.
    """

    hyperparameter_defaults = network_hyperparameter_defaults.extend(
        compile_hyperparameter_defaults).extend(
        input_encoding_hyperparameter_defaults).extend(
        fit_hyperparameter_defaults).extend(
        early_stopping_hyperparameter_defaults)
    """
    Combined set of all supported hyperparameters and their default values.
    """

    def __init__(self, **hyperparameters):
        self.hyperparameters = self.hyperparameter_defaults.with_defaults(
            hyperparameters)

        self._network = None
        self.network_json = None
        self.network_weights = None

        self.loss_history = None
        self.fit_seconds = None
        self.fit_num_points = None

    KERAS_MODELS_CACHE = {}
    """
    Process-wide keras model cache, a map from: architecture JSON string to
    (Keras model, existing network weights)
    """

    @classmethod
    def borrow_cached_network(klass, network_json, network_weights):
        """
        Return a keras Model with the specified architecture and weights.
        As an optimization, when possible this will reuse architectures from a
        process-wide cache.

        The returned object is "borrowed" in the sense that its weights can
        change later after subsequent calls to this method from other objects.

        If you're using this from a parallel implementation you'll need to
        hold a lock while using the returned object.

        Parameters
        ----------
        network_json : string of JSON
        network_weights : list of numpy.array

        Returns
        -------
        keras.models.Model
        """
        assert network_weights is not None
        if network_json not in klass.KERAS_MODELS_CACHE:
            # Cache miss.
            import keras.models
            network = keras.models.model_from_json(network_json)
            existing_weights = None
        else:
            # Cache hit.
            (network, existing_weights) = klass.KERAS_MODELS_CACHE[network_json]
        if existing_weights is not network_weights:
            network.set_weights(network_weights)
            klass.KERAS_MODELS_CACHE[network_json] = (network, network_weights)
        return network

    def network(self, borrow=False):
        """
        Return the keras model associated with this predictor.

        Parameters
        ----------
        borrow : bool
            Whether to return a cached model if possible. See
            borrow_cached_network for details

        Returns
        -------
        keras.models.Model
        """
        if self._network is None and self.network_json is not None:
            if borrow:
                return self.borrow_cached_network(
                    self.network_json,
                    self.network_weights)
            else:
                import keras.models
                self._network = keras.models.model_from_json(self.network_json)
                if self.network_weights is not None:
                    self._network.set_weights(self.network_weights)
                self.network_json = None
                self.network_weights = None
        return self._network

    def update_network_description(self):
        if self._network is not None:
            self.network_json = self._network.to_json()
            self.network_weights = self._network.get_weights()

    def get_config(self):
        """
        serialize to a dict all attributes except model weights
        
        Returns
        -------
        dict
        """
        self.update_network_description()
        result = dict(self.__dict__)
        result['_network'] = None
        result['network_weights'] = None
        return result

    @classmethod
    def from_config(cls, config, weights=None):
        """
        deserialize from a dict returned by get_config().
        
        Parameters
        ----------
        config : dict
        weights : list of array, optional
            Network weights to restore

        Returns
        -------
        Class1NeuralNetwork
        """
        config = dict(config)
        instance = cls(**config.pop('hyperparameters'))
        assert all(hasattr(instance, key) for key in config), config.keys()
        instance.__dict__.update(config)
        instance.network_weights = weights
        return instance

    def get_weights(self):
        """
        Get the network weights
        
        Returns
        -------
        list of numpy.array giving weights for each layer
        or None if there is no network
        """
        self.update_network_description()
        return self.network_weights

    def __getstate__(self):
        """
        serialize to a dict. Model weights are included. For pickle support.
        
        Returns
        -------
        dict

        """
        self.update_network_description()
        self.update_network_description()
        result = dict(self.__dict__)
        result['_network'] = None
        return result

    def peptides_to_network_input(self, peptides):
        """
        Encode peptides to the fixed-length encoding expected by the neural
        network (which depends on the architecture).
        
        Parameters
        ----------
        peptides : EncodableSequences or list of string

        Returns
        -------
        numpy.array
        """
        encoder = EncodableSequences.create(peptides)
        if (self.hyperparameters['use_embedding'] or
                self.hyperparameters['peptide_amino_acid_encoding'] == "embedding"):
            encoded = encoder.variable_length_to_fixed_length_categorical(
                max_length=self.hyperparameters['kmer_size'],
                **self.input_encoding_hyperparameter_defaults.subselect(
                    self.hyperparameters))
        elif (
                self.hyperparameters['peptide_amino_acid_encoding'] in
                    available_vector_encodings()):
            encoded = encoder.variable_length_to_fixed_length_vector_encoding(
                self.hyperparameters['peptide_amino_acid_encoding'],
                max_length=self.hyperparameters['kmer_size'],
                **self.input_encoding_hyperparameter_defaults.subselect(
                    self.hyperparameters))
        else:
            raise ValueError("Unsupported peptide_amino_acid_encoding: %s" %
                             self.hyperparameters['peptide_amino_acid_encoding'])
        assert len(encoded) == len(peptides)
        return encoded

    @property
    def supported_peptide_lengths(self):
        """
        (minimum, maximum) lengths of peptides supported, inclusive.
        
        Returns
        -------
        (int, int) tuple

        """
        return (
            self.hyperparameters['left_edge'] +
            self.hyperparameters['right_edge'],
        self.hyperparameters['kmer_size'])

    def pseudosequence_to_network_input(self, pseudosequences):
        """
        Encode pseudosequences to the fixed-length encoding expected by the neural
        network (which depends on the architecture).

        Parameters
        ----------
        pseudosequences : EncodableSequences or list of string

        Returns
        -------
        numpy.array
        """
        encoder = EncodableSequences.create(pseudosequences)
        if self.hyperparameters['pseudosequence_use_embedding']:
            encoded = encoder.fixed_length_categorical()
        else:
            raise NotImplementedError
            # encoded = encoder.fixed_length_one_hot()
        assert len(encoded) == len(pseudosequences)
        return encoded

    def fit(
            self,
            peptides,
            affinities,
            allele_pseudosequences=None,
            sample_weights=None,
            verbose=1,
            progress_preamble=""):
        """
        Fit the neural network.
        
        Parameters
        ----------
        peptides : EncodableSequences or list of string
        
        affinities : list of float
            nM affinities. Must be same length of as peptides.
        
        allele_pseudosequences : EncodableSequences or list of string, optional
            If not specified, the model will be a single-allele predictor.
            
        sample_weights : list of float, optional
            If not specified, all samples (including random negatives added
            during training) will have equal weight. If specified, the random
            negatives will be assigned weight=1.0.
        
        verbose : int
            Keras verbosity level

        progress_preamble : string
            Optional string of information to include in each progress update
        """

        self.fit_num_points = len(peptides)

        encodable_peptides = EncodableSequences.create(peptides)
        peptide_encoding = self.peptides_to_network_input(encodable_peptides)

        length_counts = (
            pandas.Series(encodable_peptides.sequences)
            .str.len().value_counts().to_dict())

        num_random_negative = {}
        for length in range(8, 16):
            num_random_negative[length] = int(
                length_counts.get(length, 0) *
                self.hyperparameters['random_negative_rate'] +
                self.hyperparameters['random_negative_constant'])
        num_random_negative = pandas.Series(num_random_negative)
        logging.info("Random negative counts per length:\n%s" % (
            str(num_random_negative.to_dict())))

        aa_distribution = None
        if self.hyperparameters['random_negative_match_distribution']:
            aa_distribution = amino_acid_distribution(
                encodable_peptides.sequences,
                smoothing=self.hyperparameters[
                    'random_negative_distribution_smoothing'])
            logging.info(
                "Using amino acid distribution for random negative:\n%s" % (
                str(aa_distribution.to_dict())))

        y_values = from_ic50(affinities)
        assert numpy.isnan(y_values).sum() == 0, numpy.isnan(y_values).sum()

        x_dict_without_random_negatives = {
            'peptide': peptide_encoding,
        }
        pseudosequence_length = None
        if allele_pseudosequences is not None:
            pseudosequences_input = self.pseudosequence_to_network_input(
                allele_pseudosequences)
            pseudosequence_length = len(pseudosequences_input[0])
            x_dict_without_random_negatives['pseudosequence'] = (
                pseudosequences_input)

        if self.network() is None:
            self._network = self.make_network(
                pseudosequence_length=pseudosequence_length,
                **self.network_hyperparameter_defaults.subselect(
                    self.hyperparameters))
            self.compile()

        y_dict_with_random_negatives = {
            "output": numpy.concatenate([
                from_ic50(
                    numpy.random.uniform(
                        self.hyperparameters[
                            'random_negative_affinity_min'],
                        self.hyperparameters[
                            'random_negative_affinity_max'],
                        int(num_random_negative.sum()))),
                y_values,
            ]),
        }
        if sample_weights is not None:
            sample_weights_with_random_negatives = numpy.concatenate([
                numpy.ones(int(num_random_negative.sum())),
                sample_weights])
        else:
            sample_weights_with_random_negatives = None

        val_losses = []
        min_val_loss_iteration = None
        min_val_loss = None

        self.loss_history = collections.defaultdict(list)
        start = time.time()
        last_progress_print = None
        for i in range(self.hyperparameters['max_epochs']):
            random_negative_peptides_list = []
            for (length, count) in num_random_negative.iteritems():
                random_negative_peptides_list.extend(
                    random_peptides(
                        count,
                        length=length,
                        distribution=aa_distribution))
            random_negative_peptides_encoding = (
                self.peptides_to_network_input(
                    random_negative_peptides_list))

            x_dict_with_random_negatives = {
                "peptide": numpy.concatenate([
                    random_negative_peptides_encoding,
                    peptide_encoding,
                ]) if len(random_negative_peptides_encoding) > 0
                else peptide_encoding
            }
            if pseudosequence_length:
                # TODO: add random pseudosequences for random negative peptides
                raise NotImplementedError(
                    "Allele pseudosequences unsupported with random negatives")

            fit_history = self.network().fit(
                x_dict_with_random_negatives,
                y_dict_with_random_negatives,
                shuffle=True,
                batch_size=self.hyperparameters['minibatch_size'],
                verbose=verbose,
                epochs=1,
                validation_split=self.hyperparameters['validation_split'],
                sample_weight=sample_weights_with_random_negatives)

            for (key, value) in fit_history.history.items():
                self.loss_history[key].extend(value)

            # Print progress no more often than once every few seconds.
            if not last_progress_print or time.time() - last_progress_print > 5:
                print((progress_preamble + " " +
                       "Epoch %3d / %3d: loss=%g. "
                       "Min val loss (%s) at epoch %s" % (
                           i,
                           self.hyperparameters['max_epochs'],
                           self.loss_history['loss'][-1],
                           str(min_val_loss),
                           min_val_loss_iteration)).strip())
                last_progress_print = time.time()

            if self.hyperparameters['validation_split']:
                val_loss = self.loss_history['val_loss'][-1]
                val_losses.append(val_loss)

                if min_val_loss is None or val_loss <= min_val_loss:
                    min_val_loss = val_loss
                    min_val_loss_iteration = i

                if self.hyperparameters['early_stopping']:
                    threshold = (
                        min_val_loss_iteration +
                        self.hyperparameters['patience'])
                    if i > threshold:
                        print((progress_preamble + " " +
                            "Early stopping at epoch %3d / %3d: loss=%g. "
                            "Min val loss (%s) at epoch %s" % (
                                i,
                                self.hyperparameters['max_epochs'],
                                self.loss_history['loss'][-1],
                                str(min_val_loss),
                                min_val_loss_iteration)).strip())
                        break
        self.fit_seconds = time.time() - start

    def predict(self, peptides, allele_pseudosequences=None, batch_size=4096):
        """
        Predict affinities
        
        Parameters
        ----------
        peptides : EncodableSequences or list of string
        
        allele_pseudosequences : EncodableSequences or list of string, optional
            Only required when this model is a pan-allele model

        batch_size : int
            batch_size passed to Keras

        Returns
        -------
        numpy.array of nM affinity predictions 
        """
        x_dict = {
            'peptide': self.peptides_to_network_input(peptides)
        }
        if allele_pseudosequences is not None:
            pseudosequences_input = self.pseudosequence_to_network_input(
                allele_pseudosequences)
            x_dict['pseudosequence'] = pseudosequences_input

        network = self.network(borrow=True)
        raw_predictions = network.predict(x_dict, batch_size=batch_size)
        predictions = numpy.array(raw_predictions, dtype = "float64")[:,0]
        return to_ic50(predictions)

    def compile(self):
        """
        Compile the keras model. Used internally.
        """
        self.network().compile(
            **self.compile_hyperparameter_defaults.subselect(
                self.hyperparameters))

    @staticmethod
    def make_network(
            pseudosequence_length,
            kmer_size,
            peptide_amino_acid_encoding,
            use_embedding,
            embedding_input_dim,
            embedding_output_dim,
            pseudosequence_use_embedding,
            layer_sizes,
            dense_layer_l1_regularization,
            dense_layer_l2_regularization,
            activation,
            init,
            output_activation,
            dropout_probability,
            batch_normalization,
            embedding_init_method,
            locally_connected_layers):
        """
        Helper function to make a keras network for class1 affinity prediction.
        """

        # We import keras here to avoid tensorflow debug output, etc. unless we
        # are actually about to use Keras.

        from keras.layers import Input
        import keras.layers
        from keras.layers.core import Dense, Flatten, Dropout
        from keras.layers.embeddings import Embedding
        from keras.layers.normalization import BatchNormalization

        if use_embedding or peptide_amino_acid_encoding == "embedding":
            peptide_input = Input(
                shape=(kmer_size,), dtype='int32', name='peptide')
            current_layer = Embedding(
                input_dim=embedding_input_dim,
                output_dim=embedding_output_dim,
                input_length=kmer_size,
                embeddings_initializer=embedding_init_method,
                name="peptide_embedding")(peptide_input)
        else:
            peptide_input = Input(
                shape=(
                    kmer_size,
                    vector_encoding_length(peptide_amino_acid_encoding)),
                dtype='float32',
                name='peptide')
            current_layer = peptide_input

        inputs = [peptide_input]

        for (i, locally_connected_params) in enumerate(locally_connected_layers):
            current_layer = keras.layers.LocallyConnected1D(
                name="lc_%d" % i,
                **locally_connected_params)(current_layer)

        current_layer = Flatten(name="flattened_0")(current_layer)

        if batch_normalization:
            current_layer = BatchNormalization(name="batch_norm_early")(
                current_layer)

        if dropout_probability:
            current_layer = Dropout(dropout_probability, name="dropout_early")(
                current_layer)

        if pseudosequence_length:
            if pseudosequence_use_embedding:
                pseudosequence_input = Input(
                    shape=(pseudosequence_length,),
                    dtype='int32',
                    name='pseudosequence')
                pseudo_embedding_layer = Embedding(
                    input_dim=embedding_input_dim,
                    output_dim=embedding_output_dim,
                    input_length=pseudosequence_length,
                    embeddings_initializer=embedding_init_method)(
                    pseudosequence_input)
            else:
                pseudosequence_input = Input(
                    shape=(pseudosequence_length, 21),
                    dtype='float32', name='peptide')
                pseudo_embedding_layer = pseudosequence_input
            inputs.append(pseudosequence_input)
            pseudo_embedding_layer = Flatten(name="flattened_1")(
                pseudo_embedding_layer)

            current_layer = keras.layers.concatenate([
                current_layer, pseudo_embedding_layer], name="concatenated_0")
            
        for (i, layer_size) in enumerate(layer_sizes):
            kernel_regularizer = None
            l1 = dense_layer_l1_regularization
            l2 = dense_layer_l2_regularization
            if l1 > 0 or l2 > 0:
                kernel_regularizer = keras.regularizers.l1_l2(l1, l2)

            current_layer = Dense(
                layer_size,
                activation=activation,
                kernel_regularizer=kernel_regularizer,
                name="dense_%d" % i)(current_layer)

            if batch_normalization:
                current_layer = BatchNormalization(name="batch_norm_%d" % i)\
                    (current_layer)

            if dropout_probability > 0:
                current_layer = Dropout(
                    dropout_probability, name="dropout_%d" % i)(current_layer)

        output = Dense(
            1,
            kernel_initializer=init,
            activation=output_activation,
            name="output")(current_layer)
        model = keras.models.Model(
            inputs=inputs,
            outputs=[output],
            name="predictor")
        return model
