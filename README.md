# Classification Metrics
Script for evaluating classification models. It's designed to be fully compatible with DVC.

## Usage
```bash
./evaluate.sh 
    --predicted path/to/predictions/file
    --true path/to/ground/truth/file
    --output-dir diretory/where/output/will/be/stored
    --format <prob or discrete>
    --binary <true_if_predictions_is_binary>
```
or just use provided dvc
```
dvc repro
```

## View metrics / plots
Formats are DVC compatible, so just use
```
dvc plots show
```
and
```
dvc metrics show
```
```
dvc metrics diff
```

## Formats
Predicted file can be in 2 formats: `prob` or `discrete`. Format `discrete` provides only a single class per sample assigned by the model. Format `prob` specified probabilities to each class in each sample assigned by the model. Examples of each format can be found in `example-data`