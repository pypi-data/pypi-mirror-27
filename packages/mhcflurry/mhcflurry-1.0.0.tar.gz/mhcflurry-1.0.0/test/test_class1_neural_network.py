import numpy
import pandas
numpy.random.seed(0)

from mhcflurry.class1_neural_network import Class1NeuralNetwork

from nose.tools import eq_
from numpy import testing

from mhcflurry.downloads import get_path


def test_class1_affinity_predictor_a0205_training_accuracy():
    # Memorize the dataset.
    hyperparameters = dict(
        activation="tanh",
        layer_sizes=[16],
        max_epochs=500,
        early_stopping=False,
        validation_split=0.0,
        locally_connected_layers=[
            {
                "filters": 8,
                "activation": "tanh",
                "kernel_size": 3
            }
        ],
        dense_layer_l1_regularization=0.0,
        dropout_probability=0.0)

    # First test a Class1NeuralNetwork, then a Class1AffinityPredictor.
    allele = "HLA-A*02:05"

    df = pandas.read_csv(
        get_path(
            "data_curated", "curated_training_data.csv.bz2"))
    df = df.ix[
        df.allele == allele
    ]
    df = df.ix[
        df.peptide.str.len() == 9
    ]
    df = df.ix[
        df.measurement_type == "quantitative"
    ]
    df = df.ix[
        df.measurement_source == "kim2014"
    ]

    predictor = Class1NeuralNetwork(**hyperparameters)
    predictor.fit(df.peptide.values, df.measurement_value.values)
    ic50_pred = predictor.predict(df.peptide.values)
    ic50_true = df.measurement_value.values
    eq_(len(ic50_pred), len(ic50_true))
    testing.assert_allclose(
        numpy.log(ic50_pred),
        numpy.log(ic50_true),
        rtol=0.2,
        atol=0.2)

    # Test that a second predictor has the same architecture json.
    # This is important for an optimization we use to re-use predictors of the
    # same architecture at prediction time.
    hyperparameters2 = dict(
        activation="tanh",
        layer_sizes=[16],
        max_epochs=1,
        early_stopping=False,
        validation_split=0.0,
        locally_connected_layers=[
            {
                "filters": 8,
                "activation": "tanh",
                "kernel_size": 3
            }
        ],
        dense_layer_l1_regularization=0.0,
        dropout_probability=0.0)
    predictor2 = Class1NeuralNetwork(**hyperparameters2)
    predictor2.fit(df.peptide.values, df.measurement_value.values)
    eq_(predictor.network().to_json(), predictor2.network().to_json())

