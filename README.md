# Wavemeter-Evaluation
Tools to evaluate measurement data from a HighFinesse Wavemeter

## Installation
Download or clone repository and:
````
python setup.py install
````
Or via pip:
````
pip install https://github.com/kricki/Wavemeter-Evaluation/archive/master.zip
````


## Example
````python
from wavemeter_evaluation import WavemeterEvaluation

wme = WavemeterEvaluation()
wme.add_data_from_file('datafile.lta')

wme.calculate_statistics(kind='frequency', print_output=True)
````
Output (Example):
````
Frequency statistics:
--------------------------------
Mean: 740345.0577011025 GHz
Standard deviation: 0.13612693591230068 GHz
Minimum value: 740344.7622132149 GHz
Maximum value: 740345.2684696611 GHz
Delta(max, min): 0.5062564462423325 GHz
--------------------------------
````