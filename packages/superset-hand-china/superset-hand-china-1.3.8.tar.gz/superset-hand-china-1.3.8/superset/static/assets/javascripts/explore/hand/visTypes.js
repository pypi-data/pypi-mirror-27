import { t } from '../../locales';

export const visTypes = {
  filter_box: {
    label: t('Filter Box'),
    controlPanelSections: [
      {
        label: t('Filter Options'),
        expanded: true,
        controlSetRows: [
          ['date_filter', 'instant_filtering'],
          ['groupby'],
          ['metric'],
        ],
      },
      {
        label: t('Setting Options'),
        expanded: true,
        controlSetRows: [
          ['show_modal']
        ]
      },
      {
        label: t('Base Setting'),
        controlSetRows: [
          ['filterSetting'],
        ]
      },
      {
        label: t('Set Default Value'),
        controlSetRows: [
          ['defaultValueSetting'],
        ]
      },
      {
        label: t('Set Date Value'),
        controlSetRows: [
          ['dateValueSetting'],
        ]
      },
    ],
    controlOverrides: {
      groupby: {
        label: t('Filter Controls'),
        description: (
          t('The controls you want to filter on. Note that only columns ' +
          'checked as "filterable" will show up on this list.')
        ),
        mapStateToProps: state => ({
          options: (state.datasource) ? state.datasource.columns.filter(c => c.filterable) : [],
        }),
      },
    },
  },
  filter_box_tree: {
    label: t('Filter Box Tree'),
    controlPanelSections: [
      {
        label: t('Metrics And Dimensions'),
        expanded: true,
        controlSetRows: [
          ['groupby', 'metrics'],
          ['parent_id', 'child_id'],
          ['child_name'],
          ['filter_name', 'width'],
          ['instant_filtering', 'multi'],
        ]
      },
      {
        label: t('Setting Options'),
        expanded: true,
        controlSetRows: [
          ['show_modal']
        ]
      },
      {
        label: t('Set Default Value Filter Tree'),
        controlSetRows: [
          ['defaultValueFilterTreeSetting'],
        ]
      },
    ]
  },
  filter_box_combination: {
    label: t('Filter Box Combination'),
    controlPanelSections: [
      {
        label: t('Filter Combination'),
        expanded: true,
        controlSetRows: [
          ['filter_combination'],
        ]
      },
    ]
  },
  // filter_box_cascade: {
  //   label: t('Filter Box Cascade'),
  //   controlPanelSections: [
  //     {
  //       label: t('Cascade Options'),
  //       expanded: true,
  //       controlSetRows: [
  //         ['groupby', 'metric'],
  //         ['width'],
  //         ['instant_filtering'],
  //       ]
  //     },
  //     {
  //       label: t('Setting Options'),
  //       expanded: true,
  //       controlSetRows: [
  //         ['show_modal']
  //       ]
  //     },
  //     {
  //       label: t('Cascade Setting'),
  //       controlSetRows: [
  //         ['cascade'],
  //       ]
  //     },
  //     {
  //       label: t('Set Default Value'),
  //       controlSetRows: [
  //         ['defaultValueSetting'],
  //       ]
  //     },
  //   ]
  // },
  ag_grid: {
    label: t('Ag-Grid'),
    controlPanelSections: [
      {
        label: t('Chart Options'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
        ]
      },
      {
        label: t('AgGrid Options'),
        expanded: false,
        controlSetRows: [
          ['order_by_cols'],
          ['row_limit'],
          ['hide_options'],
        ]
      },
      {
        label: t('Setting Options'),
        expanded: true,
        controlSetRows: [
          ['show_modal']
        ]
      },
      {
        label: t('Base Style'),
        controlSetRows: [
          ['table_style'],
          ['col_style']
        ]
      },
      {
        label: t('Condition'),
        controlSetRows: [
          ['condition_style']
        ]
      },
      {
        label: t('Compare'),
        controlSetRows: [
          ['compare_style']
        ]
      },
      {
        label: t('Navigator'),
        controlSetRows: [
          ['navigator']
        ]
      },
      {
        label: t('agGrid'),
        controlSetRows: [
          ['theme', 'pageSize'],
          ['frozen_left', 'frozen_right'],
          ['link_cols', 'hide_cols'],
          ['is_pivot'],
          ['parent_node']
        ]
      },
      {
        label: t('agGrid Pivot'),
        controlSetRows: [
          ['pivot_groupby'],
          ['columns'],
          ['pivot_metrics']
        ]
      }
    ]
  },
  echarts_bar_progress: {
    label: t('Echarts - Bar Progress'),
    controlPanelSections: [
      {
        label: t('Metrics And Dimensions'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
          ['order_by_cols'],
          ['row_limit'],
        ]
      },
      {
        label: t('Only Bottom X Options'),
        expanded: true,
        controlSetRows: [
          ['x_format', 'x_degree'],
          ['x_axis_name'],
        ]
      },
      {
        label: t('Padding Options'),
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
          ['bar_width'],
        ]
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['enabled_bar_width'],
        ]
      },
      {
        label: t('Bar Stacks'),
        expanded: true,
        description: t('bar stacks'),
        controlSetRows: [['stacks']],
      }
    ],
    controlOverrides: {
      groupby: {
        label: t('Y Axis'),
        description: t('One or many fields to group by'),
      },
    },
  },
  echarts_bar: {
    label: t('Echarts - Bar Chart'),
    controlPanelSections: [
      {
        label: t('Chart Options'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
          ['order_by_cols'],
          ['row_limit'],
        ]
      },
      {
        label: t('Only Left Options'),
        expanded: true,
        controlSetRows: [
          ['only_left', 'y_metrics'],
          ['y_format', 'y_degree'],
          ['y_axis_name'],
        ]
      },
      {
        label: t('Multi Y Axis Options'),
        controlSetRows: [
          ['y_left_metrics', 'y_right_metrics'],
          ['y_left_format', 'y_right_format'],
          ['y_left_degree', 'y_right_degree'],
          ['y_left_splitLine', 'y_right_splitLine']
        ]
      },
      {
        label: t('Padding Options'),
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
          ['bar_width'],
        ]
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['is_avg', 'is_max_min'],
          ['is_bar_value', 'enabled_bar_width'],
          ['show_all_axisLabel'],
        ]
      },
      {
        label: t('Bar Stacks'),
        expanded: true,
        description: t('bar stacks'),
        controlSetRows: [['stacks']],
      },
    ],
    // controlOverrides: {
    //   groupby: {
    //     label: 'Series',
    //   },
    //   columns: {
    //     label: 'Breakdowns',
    //     description: 'Defines how each series is broken down',
    //   },
    // },
  },
  echarts_pictorial_bar: {
    label: t('Echarts - Pictorial Bar'),
    controlPanelSections: [
      {
        label: t('Chart Options'),
        expanded: true,
        controlSetRows: [
          ['groupby_one','metric'],
          ['order_type'],
          ['icon_multi_select'],
        ]
      },
      {
        label: t('Padding Options'),
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
        ]
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['show_all_axisLabel'],
        ]
      },  
    ],
  },
  echarts_bar_waterfall: {
    label: t('Echarts - Bar Waterfall'),
    controlPanelSections: [
      {
        label: t('Metrics And Dimensions'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['order_by_cols'],
          ['row_limit'],
        ]
      },
      {
        label: t('Padding'),
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
          ['y_format', 'y_degree'],
          ['y_axis_name'],
          ['bar_width'],
        ],
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['enabled_bar_width','show_all_axisLabel'],
        ]
      },
    ]
  },
  echarts_bar_h: {
    label: t('Echarts - Bar Chart Horizontal'),
    controlPanelSections: [
      {
        label: t('Chart Options'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
          ['order_by_cols'],
          ['row_limit'],
        ]
      },
      {
        label: t('Only Bottom Options'),
        expanded: true,
        controlSetRows: [
          ['only_bottom', 'x_metrics'],
          ['x_format', 'x_degree'],
          ['x_axis_name'],
        ]
      },
      {
        label: t('Multi X Axis Options'),
        controlSetRows: [
          ['x_bottom_metrics', 'x_top_metrics'],
          ['x_bottom_format', 'x_top_format'],
          ['x_bottom_degree', 'x_top_degree'],
        ]
      },
      {
        label: t('Padding Options'),
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
          ['bar_width'],
        ]
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['is_avg', 'is_max_min'],
          ['is_bar_value', 'enabled_bar_width'],
        ]
      },
      {
        label: t('Bar Stacks'),
        expanded: true,
        description: t('bar stacks'),
        controlSetRows: [['stacks']],
      },
    ]
  },
  echarts_line_bar: {
    label: t('Echarts - Line Bar'),
    controlPanelSections: [
      {
        label: t('Metrics And Dimensions'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
          ['order_by_cols'],
          ['row_limit'],
        ]
      },
      {
        label: t('Line and Bar'),
        controlSetRows: [
          ['line_choice'],
        ]
      },
      {
        label: t('Only Left Options'),
        expanded: true,
        controlSetRows: [
          ['only_left', 'y_metrics'],
          ['y_format', 'y_degree'],
          ['y_axis_name'],
        ]
      },
      {
        label: t('Multi Y Axis Options'),
        controlSetRows: [
          ['y_left_metrics', 'y_right_metrics'],
          ['y_left_format', 'y_right_format'],
          ['y_left_degree', 'y_right_degree'],
          ['y_left_splitLine', 'y_right_splitLine'],
        ]
      },
      {
        label: t('Padding Options'),
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
          ['bar_width'],
        ]
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['is_avg', 'is_max_min'],
          ['is_bar_value', 'enabled_bar_width'],
          ['show_all_axisLabel'],
        ]
      },
      {
        label: t('Bar Stacks'),
        expanded: true,
        description: t('bar stacks'),
        controlSetRows: [['stacks']],
      },
    ],
    controlOverrides: {
      groupby: {
        label: t('Y Axis'),
        description: t('One or many fields to group by'),
      },
    },
  },
  echarts_line: {
    label: t('Echarts - Line'),
    controlPanelSections: [
      {
        label: t('Chart Options'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
          ['order_by_cols'],
          ['row_limit'],
        ]
      },
      {
        label: t('Only Left Options'),
        expanded: true,
        controlSetRows: [
          ['only_left', 'y_metrics'],
          ['y_format', 'y_degree'],
          ['y_axis_name'],
        ]
      },
      {
        label: t('Multi Y Axis Options'),
        controlSetRows: [
          ['y_left_metrics', 'y_right_metrics'],
          ['y_left_format', 'y_right_format'],
          ['y_left_degree', 'y_right_degree'],
          ['y_left_splitLine', 'y_right_splitLine']
        ]
      },
      {
        label: t('Padding Options'),
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
        ]
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['is_avg', 'is_max_min'],
          ['is_bar_value','show_all_axisLabel'],
        ]
      },
    ]
  },
  echarts_pie_m: {
    label: t('Echarts - Pie Metrics'),
    controlPanelSections: [
      {
        label: t('Metrics'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['order_by_cols'],
          ['row_limit'],

        ]
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['label_position', 'label_format'],
          ['circle_type', 'rose_type'],
        ],
      },
    ]
  },
  echarts_pie_h: {
    label: t('Echarts - Echarts Pie H'),
    controlPanelSections: [
      {
        label: t('Metrics Options'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['order_by_cols'],
          ['row_limit'],
          
        ]
      },
      {
        label: t('Inner Circle'),
        expanded: true,
        controlSetRows: [
          ['inner_metrics'],
          ['inner_label_position', 'inner_label_format'],
          ['inner_lable_color'],
        ]
      },
      {
        label: t('Outer Circle'),
        expanded: true,
        controlSetRows: [
          ['outer_metrics'],
          ['outer_label_position', 'outer_label_format'],
        ]
      },
    ]
  },
  echarts_pie_g: {
    label: t('Echarts - Pie GroupBy'),
    controlPanelSections: [
      {
        label: t('Metrics'),
        expanded: true,
        controlSetRows: [
          ['groupby', 'metrics'],
          ['order_by_cols'],
          ['row_limit'],
          ['display_limit'],
          ['other_options_name'],
        ]
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['label_position', 'label_format'],
          ['circle_type', 'rose_type'],
          ['col_num']
        ],
      },
    ]
  },

  echarts_pie_h_g: {
    label: t('Echarts - Pie H GroupBy'),
    controlPanelSections: [
      {
        label: t('Metrics Options'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['order_by_cols'],
          ['col_num'],
          ['row_limit'],
        ]
      },
      {
        label: t('Inner Circle'),
        expanded: true,
        controlSetRows: [
          ['inner_metrics_one'],
          ['inner_label_position', 'inner_label_format'],
          ['inner_lable_color'],
          ['display_limit'],
          ['other_options_name'],
        ]
      },
      {
        label: t('Outer Circle'),
        expanded: true,
        controlSetRows: [
          ['outer_metrics_one'],
          ['outer_label_position', 'outer_label_format'],
        ]
      },
    ]
  },
  echarts_multiple_ring_diagram: {
    label: t('Echarts - Multiple Ring Diagram'),
    controlPanelSections: [
      {
        label: t('Metrics And Dimensions'),
        expanded: true,
        controlSetRows: [
          ['metric','metrics'],
          ['subheader', 'fontSize'],
          ['format'],
        ]
      },
    ]
  },
  echarts_dash_board: {
    label: t('Echarts - Dash Board'),
    controlPanelSections: [
      {
        label: t('Metrics Options'),
        expanded: true,
        controlSetRows: [
          ['metric'],
          ['row_limit'],
        ]
      },
      {
        label: t('Other Option'),
        controlSetRows: [
          ['dash_min', 'dash_max'],
          ['dash_name', 'dash_splitNum'],
          ['dash_expr', 'dash_suffix'],
          ['dash_style']
        ]
      },
    ]
  },
  echarts_big_number_compare: {
    label: t('Echarts - Big Number Compare'),
    controlPanelSections: [
      {
        label: t('Metrics And Dimensions'),
        expanded: true,
        controlSetRows: [
          ['metrics_one', 'metrics_two'],
          ['subheader', 'fontSize'],
        ]
      },
    ]
  },
  echarts_liquid_fill: {
    label: t('Echarts - Big Liquid Fill'),
    controlPanelSections: [
      {
        label: t('Metrics And Dimensions'),
        expanded: true,
        controlSetRows: [
          ['metrics_one', 'metrics_two'],
          ['shape_select'],
        ]
      },
    ]
  }, 
  echarts_big_number: {
    label: t('Echarts - Big Number'),
    controlPanelSections: [
      {
        label: t('Chart Options'),
        expanded: true,
        controlSetRows: [
          ['metric'],
          ['subheader', 'fontSize'],
        ]
      },
    ]
  },
  //big number
  big_number_viz: {
    label: t('Big Number One'),
    controlPanelSections: [
      {
        label: t('Big Number One'),
        expanded: true,
        controlSetRows: [
          ['metric'],
          ['subheader', 'titleSize'],
          ['head_color', 'body_color'],
          ['format', 'big_number_fontSize'],
          ['icone_select'],
        ]
      },
    ]
  },

  //big number two
  big_number_two_viz: {
    label: t('Big Number Two'),
    controlPanelSections: [
      {
        label: t('Big Number Two'),
        expanded: true,
        controlSetRows: [
          ['metric'],
          ['metrics_one', 'metrics_two'],
          ['format', 'big_number_fontSize'],
          ['fontColor'],
          ['number_description', 'progress_description'],
          ['icone_select'],
        ]
      },
    ]
  },
  //big number three
  big_number_three_viz: {
    label: t('Big Number Three'),
    controlPanelSections: [
      {
        label: t('Big Number Three'),
        expanded: true,
        controlSetRows: [
          ['metric'],
          ['subheader', 'number_description'],
          ['format', 'big_number_fontSize'],
          ['icon_color'],
          ['icone_select'],
        ]
      },
    ]
  },
  //big number four
  big_number_four_viz: {
    label: t('Big Number Four'),
    controlPanelSections: [
      {
        label: t('Big Number Four'),
        expanded: true,
        controlSetRows: [
          ['metric'],
          ['background_color', 'font_color'],
          ['format', 'big_number_four_fontSize'],
          ['font_weight'],
        ]
      },
      {
        label: t('Label Options'),
        controlSetRows: [
          ['label_content','label_color'],
          ['label_size', 'label_weight'],
          ['label_top_padding'],
        ]
      }
    ]
  },
  echarts_china_map: {
    label: t('China Map'),
    controlPanelSections: [
      {
        label: t('Metrics and Dimensions'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby_one'],
          ['min_legend'],
          ['max_legend'],
        ]
      },
    ]
  },

  china_city_map: {
    label: t('China City Map'),
    controlPanelSections: [
      {
        label: t('Metrics and Dimensions '),
        expanded: true,
        controlSetRows: [
          ['metric'],
          ['groupby_one'],
          ['standard_point'],
          ['china_city_format'],
        ]
      },
    ]
  },
  //echarts china city map migration
  echarts_china_city_map_migration: {
    label: t('China City Map Migration'),
    controlPanelSections: [
      {
        label: t('Metrics and Dimensions'),
        expanded: true,
        controlSetRows: [
          ['metric'],
          ['groupby'],
          ['min_legend'],
          ['max_legend'],
        ]
      },
    ],
    controlOverrides: {
      groupby: {
        label: t('From City / To City'),
        description: t('Choose a from city and a to city'),
      }
    },
  },

  echarts_bubble: {
    label: t('Echarts - Bubble'),
    controlPanelSections: [
      {
        label: t('Chart Options'),
        expanded: true,
        controlSetRows: [
          ['series', 'entity'],
          ['x', 'y'],
          ['size', 'row_limit'],
        ]
      },
      {
        label: t('X/Y Axis Options'),
        expanded: true,
        controlSetRows: [
          ['x_axis_label', 'y_axis_label'],
          ['x_degree', 'y_degree'],
          ['x_format', 'y_format'],
        ]
      },
      {
        label: t('Padding Options'),
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
        ]
      }
    ]
  },
  echarts_quadrant: {
    label: t('Echarts - Quadrant'),
    controlPanelSections: [
      {
        label: t('Chart Options'),
        expanded: true,
        controlSetRows: [
          ['series'],
          ['x_metric', 'y_metric'],
          ['row_limit'],
          ['origin_x', 'origin_y'],
          ['min_x_axis', 'max_x_axis'],
          ['min_y_axis', 'max_y_axis'],
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
          ['point_size'],
          ['first_module_infor'],
          ['first_x', 'first_y'],
          ['second_module_infor'],
          ['second_x', 'second_y'],
          ['third_module_infor'],
          ['third_x', 'third_y'],
          ['fourth_module_infor'],
          ['fourth_x', 'fourth_y'],
        ]
      },
    ]
  },

  //echarts area stack
  echarts_area_stack: {
    label: t('Echarts - Area Stack'),
    controlPanelSections: [
      {
        label: t('Area Stack Options'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
          ['order_by_cols'],
          ['row_limit'],
        ]
      },
      {
        label: t('Left Options'),
        expanded: true,
        controlSetRows: [
          ['y_metrics'],
          ['y_format', 'y_degree'],
          ['y_axis_name'],
        ]
      },
      {
        label: t('Padding Options'),
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
        ]
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['is_bar_value', 'normal'],
          ['show_all_axisLabel','lable_color'],
        ]
      },
    ]
  },

  //echarts sankey
  echarts_sankey: {
    label: t('Echarts - Sankey'),
    controlPanelSections: [
      {
        label: t('Metrics Options'),
        expanded: true,
        controlSetRows: [
          ['groupby'],
          ['metric'],
          ['row_limit'],
        ]
      }
    ],
    controlOverrides: {
      groupby: {
        label: t('Source / Target'),
        description: t('Choose a source and a target'),
      }
    },
  },


  //漏斗图
  echarts_funnel: {
    label: t('Echarts - Funnel'),
    controlPanelSections: [
      {
        label: t('Metrics Options'),
        expanded: true,
        controlSetRows: [
          ['groupby_one'],
          ['metric'],
          ['order_type'],

        ]
      },
    ]
  },
  echarts_radar_map: {
    label: t('Echarts - Radar Map'),
    controlPanelSections: [
      {
        label: t('Metrics'),
        expanded: true,
        controlSetRows: [
          ['groupby', 'metrics'],
          ['row_limit'],
        ]
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['circle', 'normal'],
        ],
      },
    ]
  },
  echarts_treemap: {
    label: t('Echarts - Treemap'),
    controlPanelSections: [
      {
        label: t('Metrics And Dimensions'),
        expanded: true,
        controlSetRows: [
          ['groupby', 'metrics'],
          ['parent_id', 'child_id'],
          ['child_name','format'],
          ['visible_min', 'leaf_depth'],
        ]
      },
    ]
  },
  echarts_word_cloud: {
    label: t('Echarts - Word Cloud'),
    controlPanelSections: [
      {
        label: t('Metrics And Dimensions'),
        expanded: true,
        controlSetRows: [
          // ['series', 'metric', 'limit'],
          ['series', 'metric'],
          ['limit'],
          ['size_from', 'size_to'],
          ['e_rotation'],
        ]
      },
    ]
  },
}