"""
Module with predefined chart settings
"""

# options
DEFAULT_OPTIONS = {
    'scales': {
        'xAxes': [{
            'gridLines': {
                'display': False
            }
        }],
        'yAxes': [{
            'ticks': {
                'min': 0,
                'max': 100,
                'stepSize': 20
            }
        }]
    },
    'maintainAspectRatio': True,
    'responsive': True,
}


LINE_CHART_OPTIONS = {
    'responsive': True,
    'tooltips': {
        'mode': 'index',
        'intersect': False
    },
    'hover': {
        'mode': 'nearest',
        'intersect': True
    },
    'scales': {
        'xAxes': [{
            'ticks': {
                'autoSkip': True,
                'maxTicksLimit': 60,  # maximum number of ticks on axis
                'display': True,
                'maxRotation': 90,
                'minRotation': 90
            },
            'scaleLabel': {
                'display': True,
                'labelString': 'Timeline'
            },
        }],
        'yAxes': [{
            'display': True,
            'scaleLabel': {
                'display': True,
                'labelString': 'Value'
            }
        }]
    }
}

LINE_CHART_DATASET_OPTIONS = {
    'fill': False
}


# chart types
class ChartType:
    LINE = 'line'
    BAR = 'bar',
