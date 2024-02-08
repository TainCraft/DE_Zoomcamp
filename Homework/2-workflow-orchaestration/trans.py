import re

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    
    data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]

    bf_data = data.columns
    af_data = [re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', col).lower() for col in data.columns]
    change=[col for col in bf_data if col not in af_data]
    print("Columns changed:", len(change))

    
    
    data.columns=af_data
    print("Values are:", data['vendor_id'].unique())

    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    return data


@test
def test_output(output, *args) -> None:
    assert (output['vendor_id'].isin([1, 2])).all(), "Assertion Error: vendor_id is not one of the existing values."
    assert (output['passenger_count'] > 0).all(), "Assertion Error: passenger_count is not greater than 0."
    assert (output['trip_distance'] > 0).all(), "Assertion Error: trip_distance is not greater than 0."
    assert output is not None, 'The output is undefined'
