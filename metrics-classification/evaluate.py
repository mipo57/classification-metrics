import json
import os
from typing import Dict, List

import click
import numpy as np
from sklearn.metrics import (classification_report, cohen_kappa_score,
                             matthews_corrcoef, roc_auc_score)


def extract_classnames(y_pred: List[Dict[str, float]]) -> List[str]:
    return list(y_pred[0].keys())


def process_probs(y_pred: List[Dict[str, float]], classnames: List[str]) -> List[List[float]]:
    return [
        [example[classname] for classname in classnames]
        for example in y_pred
    ]


def process_argmax(y_pred: List[Dict[str, float]]) -> List[str]:
    return [
        list(example.keys())[np.argmax(list(example.values()))]
        for example in y_pred
    ]


def confusion_plot(y_true: List[str], y_pred: List[str]):
    return {
        'Confusion Matrix': [{
            'predicted': p,
            'true': t
        } for t, p in zip(y_true, y_pred)]
    }


@click.command()
@click.option('--predicted', type=click.Path(exists=True, file_okay=True), required=True)
@click.option('--true', type=click.Path(exists=True, file_okay=True), required=True)
@click.option('--output-dir', type=click.Path(exists=False), default='.')
@click.option('--format', type=click.Choice(['prob', 'discrete']), default='prob')
@click.option('--binary', type=bool, default=False)
def main(predicted: str, true: str, output_dir: str, format: str, binary: bool):
    os.makedirs(output_dir, exist_ok=True)

    with open(predicted, 'r') as f:
        y_pred_dict = json.load(f)
    with open(true, 'r') as f:
        y_true_dict = json.load(f)

    y_pred = list(y_pred_dict.values())
    y_true = [y_true_dict[x] for x in y_pred_dict.keys()]

    if format == 'prob':
        classnames = extract_classnames(y_pred)
        y_pred_argmaxed = process_argmax(y_pred)
    else:
        y_pred_argmaxed = y_pred

    metrics = classification_report(y_true, y_pred_argmaxed, output_dict=True)
    metrics['cohen_kappa'] = cohen_kappa_score(y_true, y_pred_argmaxed)
    metrics['matthews'] = matthews_corrcoef(y_true, y_pred_argmaxed)

    if format == 'prob':
        y_pred_probs = process_probs(y_pred, classnames)
        metrics['roc_auc'] = roc_auc_score(
            y_true, y_pred_probs, labels=classnames, multi_class='ovo')

    with open(f'{output_dir}/metrics.json', 'w') as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    confussion = confusion_plot(y_true, y_pred_argmaxed)
    with open(f'{output_dir}/confusion.json', 'w') as f:
        json.dump(confussion, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
