import unittest
import pandas as pd
from encoder import Encoder
from pandas.util.testing import assert_frame_equal


class TestEncoder(unittest.TestCase):

    def test_fit(self):
        """Tests the fit method"""

        df = pd.DataFrame(
            data=[
                ['Name_1', 10.2, 'Address_1'],
                ['Name_2', 5, 'Address_2'],
                [None, 7, 'Address_3']],
            columns=['Name', 'Age', 'Address']
        )

        encoder = Encoder(verbose=1)
        encoder.fit(df)

        # The encoder should understand that he must encode columns Name and Age
        assert len(encoder.categories_by_column) == 2
        assert list(encoder.categories_by_column['Name']) == ['Name_1', 'Name_2']
        assert list(encoder.categories_by_column['Address']) == ['Address_1', 'Address_2', 'Address_3']

    def test_fit_with_na(self):
        """Tests the fit method when we have nan values"""

        df = pd.DataFrame(
            data=[
                ['Name_1', 10.0, 'Address_1'],
                ['Name_2', 10.5, 'Address_2'],
                [None, 7, 'Address_3']],
            columns=['Name', 'Age', 'Address']
        )

        encoder = Encoder(dummy_na=True)
        encoder.fit(df, columns=['Name'])

        # The encoder should understand that he must encode columns Name and Age
        assert len(encoder.categories_by_column) == 1
        assert list(encoder.categories_by_column['Name']) == ['Name_1', 'Name_2', None]

    def test_get_dummies(self):
        """Tests get dummies"""
        df = pd.DataFrame(
            data=[
                ['Name_1', 10.0, 'Address_1'],
                ['Name_2', 10.5, 'Address_2'],
                ['Name_1', 7, 'Address_3']],
            columns=['Name', 'Age', 'Address']
        )

        encoder = Encoder()
        encoder.fit(df, columns=['Name'])
        dummies_df = encoder.get_dummies(df)

        expected_dummies_df = pd.DataFrame(
            data=[
                [10.0, 'Address_1', 1, 0],
                [10.5, 'Address_2', 0, 1],
                [7, 'Address_3', 1, 0]],
            columns=['Age', 'Address', 'Name_Name_1', 'Name_Name_2']
        )
        assert_frame_equal(dummies_df, expected_dummies_df)

    def test_get_dummies_with_duplicated_columns(self):
        """Tests get dummies without duplicating columns"""
        df = pd.DataFrame(
            data=[
                ['Name_1', 10.0, 'Address_1'],
                ['Name_2', 10.5, 'Address_2'],
                ['Name_1', 7, 'Address_3']],
            columns=['Name', 'Name_Name_1', 'Name_Name_1_0']
        )

        encoder = Encoder()
        encoder.fit(df, columns=['Name'])
        dummies_df = encoder.get_dummies(df, edit=True)

        # the column Name_Name_1 exists already: the encoder will try to create a new one.
        expected_dummies_df = pd.DataFrame(
            data=[
                [10.0, 'Address_1', 1, 0],
                [10.5, 'Address_2', 0, 1],
                [7, 'Address_3', 1, 0]],
            columns=['Name_Name_1', 'Name_Name_1_0', 'Name_Name_1_1', 'Name_Name_2']
        )
        assert_frame_equal(dummies_df, expected_dummies_df)
        # we make sure that data is modified and equal to dummies df
        assert_frame_equal(df, expected_dummies_df)

    def test_get_dummies_with_drop_first(self):
        """Tests get_dummies with dropping first columns"""
        df = pd.DataFrame(
            data=[
                ['Name_1', 10.0, 'Address_1'],
                ['Name_2', 10.5, 'Address_2'],
                ['Name_1', 7, 'Address_3']],
            columns=['Name', 'Age', 'Address']
        )

        encoder = Encoder(drop_first=True)
        encoder.fit(df, columns=['Name'], )
        dummies_df = encoder.get_dummies(df)

        # the column Name_Name_1 exists already: the encoder will try to create a new one.
        expected_dummies_df = pd.DataFrame(
            data=[
                [10.0, 'Address_1', 0],
                [10.5, 'Address_2', 1],
                [7, 'Address_3', 0]],
            columns=['Age', 'Address', 'Name_Name_2']
        )
        assert_frame_equal(dummies_df, expected_dummies_df)

    def test_get_dummies_with_test_data(self):
        """The goal of this test id to make sure that test data will always have the same columns"""
        train_data = pd.DataFrame(
            data=[
                ['Name_1', 10.0, 'Address_1'],
                ['Name_2', 10.5, 'Address_2'],
                ['Name_1', 7, 'Address_3']],
            columns=['Name', 'Age', 'Address']
        )
        encoder = Encoder(drop_first=True)
        encoder.fit(train_data, columns=['Name'])

        test_df = pd.DataFrame(
            data=[
                ['Name_3', 10.0, 'Address_1'],
                ['Name_4', 10.5, 'Address_2'],
                ['Name_1', 7, 'Address_3']],
            columns=['Name', 'Age', 'Address']
        )
        expected_test_dummies_df = pd.DataFrame(
            data=[
                [10.0, 'Address_1', 0],
                [10.5, 'Address_2', 0],
                [7, 'Address_3', 0]],
            columns=['Age', 'Address', 'Name_Name_2']
        )

        assert_frame_equal(encoder.get_dummies(test_df), expected_test_dummies_df)
