const $ = require('jquery');
import React from 'react';
import ReactDOM from 'react-dom';
import { Popover, OverlayTrigger } from 'react-bootstrap';
import d3 from 'd3';

import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-enterprise';

import 'ag-grid/dist/styles/ag-grid.css';
import 'ag-grid/dist/styles/theme-fresh.css';
import 'ag-grid/dist/styles/theme-dark.css';
import 'ag-grid/dist/styles/theme-bootstrap.css';
import 'ag-grid/dist/styles/theme-material.css';
import 'ag-grid/dist/styles/theme-blue.css';
import './ag_grid.css';
import { t } from '../../javascripts/locales';

// import navigator from './navigate.js';
const navigator = require('./navigate.js');

const propTypes = {
  form_data: React.PropTypes.object.isRequired,
  data: React.PropTypes.object.isRequired,
  height: React.PropTypes.number.isRequired,
  slice: React.PropTypes.object.isRequired,
};

class AgGrid extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      gridTheme: 'ag-' + this.props.form_data.theme,
      pageSize: this.props.form_data.pageSize,
      showToolPanel: false,
      quickFilterText: null,
      sliceName: null,
    };
    this.gridOptions = {
      pagination: !this.props.form_data.hide_options,
      paginationPageSize: parseInt(this.props.form_data.pageSize),
      rowBuffer: 10, // no need to set this, the default is fine for almost all scenarios
      floatingTopRowData: [],
      floatingBottomRowData: [],
      // columnDefs: this.initColumnDefs(),
      // rowGroupPanelShow: 'always',
      enableColResize: true,
      // pivotPanelShow: 'always',
      localeText: {
        // for filter panel
        page: t('page'),
        more: t('more'),
        to: t('to'),
        of: t('of'),
        next: t('next'),
        last: t('last'),
        first: t('first'),
        previous: t('previous'),
        loadingOoo: t('loading'),
      }
    };
    if (this.props.form_data.is_pivot !== 'true') {
      // table
      this.gridOptions.pivotMode = false;
      this.gridOptions.columnDefs = this.initTableColumnDefs();
    } else {
      // pivot table
      this.gridOptions.pivotMode = true;
      this.gridOptions.functionsReadOnly = true;
      this.gridOptions.columnDefs = this.initPivotTableColumnDefs();
    }
  }

  componentWillMount() {
    const _this = this;
    $.get('/hand/explore/getSliceName/' + this.props.form_data.slice_id, function (data) {
      _this.setState({ sliceName: data });
    });
  }

  getAllRecordsByColumnName(columnName) {
    const data = [];
    this.props.data.records.forEach(r => {
      data.push(r[columnName]);
    });
    return data;
  }

  styleArrayToJson(array, isWidth) {
    const json = {};
    array.forEach(a => {
      const k = a.split(':');
      if (k[0] !== '' && k[0] !== 'width') {
        json[k[0].trim()] = k[1].trim();
      }
    });
    return json;
  }

  initTableColumnDefs() {
    const fd = this.props.form_data;
    const navigateFunctions = navigator();
    const slice = this.props.slice;

    // get compare info from form_data
    const compareMetric1 = [];
    const compareMetric2 = [];
    const compareExprs = [];
    const compareStyles = [];
    fd.compare_style.forEach(c => {
      let newMetric1 = ''
      const ac = slice.datasource.metrics_combo;
      for(let i in ac){
        if(c.metric1 == ac[i][0]){
          newMetric1 = ac[i][1]
          break; 
        }
      } 
      let newMetric2 = ''
      for(let i in ac){
        if(c.metric2 == ac[i][0]){
          newMetric2 = ac[i][1]
          break; 
        }
      }  
      compareMetric1.push(this.getAllRecordsByColumnName(newMetric1));
      compareMetric2.push(this.getAllRecordsByColumnName(newMetric2));
      compareExprs.push(c.expr);
      compareStyles.push(c.style);
    });

    const columnDefs = [];
    // const columnNames = this.props.data.columns;
    const columnNames = fd.groupby.concat(fd.metrics);
    columnNames.forEach(columnName => {
      const _this = this;
      const props = {
        headerName: columnName,
        field: columnName,
        width: 100,
        enablePivot: true,
      };

      // set hidden
      let sh = []
      const ac = slice.datasource.all_cols.concat(slice.datasource.metrics_combo);
      for(let i in ac){
        for(let hc in fd.hide_cols){
          if(fd.hide_cols[hc] == ac[i][0])
            sh.push(ac[i][1])
        }
      }      
      if ($.inArray(columnName, sh) != -1) {
        props.hide = true;
      }

      // set pinned
      let fl = []
      for(let i in ac){
        for(let f in fd.frozen_left){
          if(fd.frozen_left[f] == ac[i][0])
            fl.push(ac[i][1]) 
      }
      }          
      if ($.inArray(columnName, fl) !== -1) {
        props.pinned = 'left';
      }
      let fr = []
      for(let i in ac){
        for(let f in fd.frozen_right){
          if(fd.frozen_right[f] == ac[i][0])
            fr.push(ac[i][1]) 
        }
      } 
      if ($.inArray(columnName, fr) !== -1) {
        props.pinned = 'right';
      }

      // set group
      fd.groupby.forEach(m => {
        if (m === columnName) {
          props.enableRowGroup = true;
          // props.pinned = true;
          return;
        }
      });

      // set aggregation
      fd.metrics.forEach(m => {
        if (m === columnName) {
          props.enableValue = true;
          return;
        }
      });

      // set header width
      fd.col_style.forEach(c => {
        let newcol = ''
            const ac = slice.datasource.all_cols.concat(slice.datasource.metrics_combo);
            for(let i in ac){
              if(c.col == ac[i][0])
                newcol = ac[i][1] 
            }        
        if (columnName === newcol) {

          // if (columnName === c.col) {
          const columnStyleArray = c.style.split(';');
          columnStyleArray.forEach(a => {
            const k = a.split(':');
            if (k[0] === 'width') {
              props.width = parseInt(k[1].substring(0, k[1].length - 2));
            }
          });
        }
      });

      props.cellStyle = function (params) {
        const styleJson = {};

        // add body style
        const bodyStyleJson = _this.styleArrayToJson(fd.table_style.split(';'), false);
        $.extend(styleJson, bodyStyleJson);

        // add column style
        fd.col_style.forEach(c => {
          let newcol = ''
          const ac = slice.datasource.all_cols.concat(slice.datasource.metrics_combo);
          for(let i in ac){
            if(c.col == ac[i][0])
              newcol = ac[i][1] 
          }                 
          if (columnName === newcol) {
            const columnStyleJson = _this.styleArrayToJson(c.style.split(';'), false);
            $.extend(styleJson, columnStyleJson);
          }
        });

        // add condition style
        fd.condition_style.forEach(c => {
            let newMetric = ''
            const ac = slice.datasource.metrics_combo;
            for(let i in ac){
              if(c.metric == ac[i][0]){
                newMetric = ac[i][1]
                break; 
              }
            }  
             if (columnName === newMetric) {
            
            //  if (columnName === c.metric) {
            let expr = c.expr.replace(/x/g, params.value);
            if (eval(expr)) {
              const conditionStylejson = _this.styleArrayToJson(c.style.split(';'));
              $.extend(styleJson, conditionStylejson);
            }
          }
        });

        // add two colums compare style
        fd.compare_style.forEach(function (c, i) {
            let newMetric1 = ''
            const ac = slice.datasource.metrics_combo;
            for(let i in ac){
              if(c.metric1 == ac[i][0]){
                newMetric1 = ac[i][1]
                break; 
              }
            }            
          // if (columnName === c.metric1) {
          if (columnName === newMetric1) {
            const expr = compareExprs[i].replace('x', compareMetric1[i][0])
              .replace('y', compareMetric2[i][0]);
            if (params.value === compareMetric1[i][0] && eval(expr)) {
              const compareStyleJson = _this.styleArrayToJson(compareStyles[i].split(';'));
              $.extend(styleJson, compareStyleJson);
            }
            // delete the first element
            // compareMetric1[i].splice(0, 1);
            // compareMetric2[i].splice(0, 1);
          }
        });
        // console.log(styleJson);
        return styleJson;
      };

      props.cellRenderer = function (params) {
        // format number
        // let value = slice.d3format(columnName, params.value);
        let value = params.value;
        if (value === '' || value === null) {
          return null;
        }
        if ($.inArray(columnName, fd.metrics) !== -1 && !isNaN(value)) {
          value = slice.d3format(columnName, params.value);
        }

        // set condition icon
        // let color = 'black';
        // for (let i = 0; i < fd.condition_style.length; i++){
        //   const c = fd.condition_style[i];
        //   if (c.metric === columnName) {
        //     let expr = c.expr.replace(/x/g, value);
        //     if (eval(expr)) {
        //       // set icon color
        //       if (c.icon === 'fa fa-arrow-up' || c.icon === 'fa fa-angle-double-up') {
        //         color = 'green;';
        //       } else if (c.icon === 'fa fa-arrow-down' || c.icon === 'fa fa-angle-double-down') {
        //         color = 'red;';
        //       }
        //       console.info(value, color, c.icon)
        //       return `{value}`
        //       // return `<span>{value}</span><i style='margin-left:20px;color:{color} 'class={c.icon} aria-hidden='true'></i>;`;
        //     }
        //   }
        // }

        // set url link
      let lc = []
      for(let i in ac){
        for(let l in fd.link_cols){
          if(fd.link_cols[l] == ac[i][0])
            lc.push(ac[i][1])
        }
      } 
        if ($.inArray(columnName, lc) !== -1) {
          return '<a target="_blank" href="' + value + '">' + t('View') + '</a>';
        }

        // set navigate link style
      
        for (let i = 0; i < fd.navigator.length; i++) {
          const n  = fd.navigator[i];
          let newNavi = ''
          const ac = slice.datasource.all_cols.concat(slice.datasource.metrics_combo);
          for(let i in ac){
            if(n.col === ac[i][0]){
              newNavi = ac[i][1]
              break
            }
          }

          if (columnName === newNavi) {
            if ($.inArray(columnName, fd.metrics) !== -1) {
              // metric navigate
              const expr = n.expr.replace(/x/g, params.value);
              if (eval(expr)) {
                return '<a href="#">' + value + '</a>';
              }
            } else {
              // groupby navigate
              return '<a href="#">' + value + '</a>';
            }
          }
        }

        return value;
      };
      props.onCellClicked = function (params) {
        // console.log(params)
        // get groupby's value
        const groupby = [];
        for (let j = 0; j < fd.groupby.length; j++) {
          groupby.push(params.data[fd.groupby[j]]);
        }
        let value = params.value;
        if (value === '' || value === null) {
          return null;
        }
        if ($.inArray(columnName, fd.metrics) !== -1 && !isNaN(value)) {
          value = slice.d3format(columnName, params.value);
        }

        const navigates = [];
        for (let i = 0; i < fd.navigator.length; i++) {
          const n = fd.navigator[i];
          let expr;
          let newNavi = ''
            const ac = slice.datasource.all_cols.concat(slice.datasource.metrics_combo);
            for(let i in ac){
              if(n.col === ac[i][0]){
                newNavi = ac[i][1]
                break
              }
          }
          if (columnName === newNavi) {
            
            if ($.inArray(columnName, fd.metrics) !== -1) {
              // metric navigate
              expr = n.expr.replace(/x/g, params.value);
            } else if ($.inArray(columnName, fd.groupby) !== -1) {
              // groupby navigate
              expr = true;
            }
            if (eval(expr)) {
              const openType = n.open_type;
              const navHeight = (n.navigate_height === '') ? '300px' : n.height;
              const navWidth = (n.navigate_width === '') ? '300px' : n.width;
              const navType = n.navigate_type;
              // navigate to dashboard
              if (navType === 'dashboard') {
                const dash = JSON.parse(
                  navigateFunctions.dashboardUrl(n.dashboard_id));
                let url = dash.url + '?standalone=true&isControl=false&isManager=false';
                const title = dash.title;
                if (url) {
                  const isFrozen = n.filter_frozen === 'true';
                  url = navigateFunctions.convertDashUrl(dash, fd.groupby, null, groupby, isFrozen);
                  const postData = {
                    url: url,
                    title: title,
                    type: openType,
                    navHeight: navHeight,
                    navWidth: navWidth,
                    isDash: true,
                  };
                  navigates.push(postData);
                  // window.parent.postMessage(postData, '*');  // send message to navigate
                }
              } else {
                // navigate to slice
                const slc = JSON.parse(navigateFunctions.sliceUrl(n.slice_id));
                let url = slc.url;
                const title = slc.title;
                if (url) {
                  const standalone = navigateFunctions.GetQueryString(url, 'standalone', []);
                  const navGroupby = navigateFunctions.GetQueryString(url, 'groupby', []);
                  const sourceGroupby = fd.groupby;
                  url = navigateFunctions.addFilter(url, sourceGroupby, navGroupby, null, groupby);
                  if (standalone.length === 0) {
                    if (url.indexOf('standalone') !== -1) {
                      url = url.replace(/standalone=/, 'standalone=true');
                    } else {
                      url += '&standalone=true';
                    }
                  }
                  const postData = {
                    url: url,
                    title: title,
                    type: openType,
                    navHeight: navHeight,
                    navWidth: navWidth,
                  };
                  navigates.push(postData);
                  // window.parent.postMessage(postData, '*');  // send message to navigate
                }
              }
            }

            // check navigates and send message to navigate
            navigateFunctions.handleNavigate(i, navigates);
          }
        }
      };

      columnDefs.push(props);
    });

    // set parentNode
    fd.parent_node.forEach(n => {
      const parentProps = {};
      parentProps.headerName = n.parentName;
      parentProps.marryChildren = true;
      parentProps.children = [];
      const ac = slice.datasource.all_cols.concat(slice.datasource.metrics_combo);
      const child = n.children.split(',')
      let childs = []
      for(let m in child){  
        for(let i in ac){
            if(child[m] === ac[i][0]){
              childs.push(ac[i][1])
            }
        }
      }
      const showitems = n.show_items.split(',')
      let  sitems = []
      for(let c in showitems){  
        for(let i in ac){
            if(showitems[c] === ac[i][0]){
              sitems.push(ac[i][1])
            }
        }
      }
      let k = 0;
      const len = columnDefs.length;
      for (let j = 0; j < len; j++) {
        if ($.inArray(columnDefs[j - k].headerName, childs) !== -1) {
          if ($.inArray(columnDefs[j - k].headerName, sitems) !== -1) {
            columnDefs[j - k].columnGroupShow = 'closed';
            parentProps.children.push(columnDefs[j - k]);
            // give close column another open column
            const openColumnObj = {};
            $.extend(openColumnObj, columnDefs[j - k]);
            openColumnObj.columnGroupShow = 'open';
            parentProps.children.push(openColumnObj);
          } else {
            columnDefs[j - k].columnGroupShow = 'open';
            parentProps.children.push(columnDefs[j - k]);
          }
          columnDefs.splice(j - k, 1);
          k++;
        }
      }
      columnDefs.push(parentProps);
    });
    return columnDefs;
  }
              
  initPivotTableColumnDefs() {
    const fd = this.props.form_data;
    const columnDefs = [];
    const sl = this.props.slice;
    fd.pivot_groupby.forEach(function (val, index) {
      const props = {
        headerName: val,
        field: val,
      };
      props.rowGroupIndex = index;
      columnDefs.push(props);
    });
    fd.columns.forEach(function (val, index) {
      let v = ''
      const ac = sl.datasource.all_cols.concat(sl.datasource.metrics_combo);
      for(let a in ac){
        if(ac[a][0] == val){
          v = ac[a][1]
        }
      }
      const props = {
        headerName: v,
        field: v,
      };
      props.pivotIndex = index;
      columnDefs.push(props);
    });
    fd.pivot_metrics.forEach(function (val) {
      const props = {
        headerName: val,
        field: val,
      };

      props.aggFunc = 'sum';
      columnDefs.push(props);
    });
    return columnDefs;
  }

  onGridReady(params) {
    this.api = params.api;
    this.columnApi = params.columnApi;
    this.createNewDatasource();
  }

  onThemeChanged(selected) {
    const themeSelected = selected.currentTarget.value;
    this.setState({ gridTheme: themeSelected });
  }

  onPageSizeChanged(selected) {
    const pageSize = new Number(selected.currentTarget.value);
    this.gridOptions.paginationPageSize = pageSize;
    this.setState({ pageSize: pageSize });
    this.createNewDatasource();
  }

  onQuickFilterText(event) {
    this.setState({ quickFilterText: event.target.value });
  }

  createNewDatasource() {
    const fd = this.props.form_data;
    const data = this.props.data;
    const columnNames = fd.groupby.concat(fd.metrics);
    const colsData = [];
    for (let i = 0; i < data.records.length; i++) {
      var colData = new Object();
      for (let j = 0; j < columnNames.length; j++) {
        colData[columnNames[j]] = data.records[i][columnNames[j]];
      }
      colsData.push(colData);
    }
    this.gridOptions.api.setRowData(colsData);
    // const total = this.props.data.total;
    // const records = this.props.data.records;
    // const pageSize = this.props.form_data.pageSize;

    // if (this.props.data.total === -1) {
    //   let dataSource = {
    //     getRows: function (params) {
    //       setTimeout(function () {
    //         let rowsThisPage = records.slice(params.startRow, params.endRow);
    //         params.successCallback(rowsThisPage, records.length);
    //       }, 500);
    //     }
    //   }
    //   this.gridOptions.api.setDatasource(dataSource);
    //   return;
    // }

    // let jsonEndpoint = this.props.slice.data.json_endpoint;
    // const re = /startRow=[\d&]*|currentPageSize=[\d&]*|total=[\d&]*/g;
    // const result = jsonEndpoint.match(re);
    // if (result != null) {
    //   result.forEach(r => {
    //     jsonEndpoint = jsonEndpoint.replace(r, '');
    //   })
    //   if (jsonEndpoint.substr(jsonEndpoint.length - 1, 1) === '&') {
    //     jsonEndpoint = jsonEndpoint.substr(0, jsonEndpoint.length - 1);
    //   }
    // }

    // let dataSource = {
    //   getRows: function (params) {
    //     // the first page
    //     if (params.startRow === 0 && params.endRow === parseInt(pageSize)) {
    //       setTimeout(function () {
    //         params.successCallback(records, total);
    //       }, 500);
    //     } else {
    //       const url = jsonEndpoint + '&startRow=' + params.startRow + '&currentPageSize=' + (params.endRow - params.startRow) + '&total=' + total;
    //       console.info(params.startRow + "         " + params.endRow);
    //       $.getJSON(url, function (json) {
    //         // let rowsThisPage = json.data.records;
    //         setTimeout(function () {
    //           let rowsThisPage = json.data.records;
    //           params.successCallback(rowsThisPage, parseInt(json.data.total));
    //         }, 500);
    //       }).fail(function () {
    //         alert('error')
    //       });
    //     }
    //   }
    // };
    // this.gridOptions.api.setDatasource(dataSource);
  }

  exportCsv() {
    const params = {
      skipHeader: false,
      columnGroups: true,
      skipFooters: true,
      skipGroups: false,
      allColumns: true,
      fileName: this.state.sliceName + '.csv'
    };
    this.gridOptions.api.exportDataAsCsv(params);
  }

  exportExcel() {
    let cols = [];
    this.gridOptions.columnApi._columnController.gridColumns.forEach(col => {
      if (col.visible) {
        cols.push(col.colDef.field);
      }
    });
    cols = $.unique(cols);
    const params = {
      skipHeader: false,
      columnGroups: true,
      skipFooters: true,
      skipGroups: false,
      allColumns: true,
      columnKeys: cols,
      fileName: this.state.sliceName
    };
    this.gridOptions.api.exportDataAsExcel(params);
  }

  renderPopover() {
    return (
      <Popover>
        <div>
          {t('If you want to export all, Please select all in the page size')}
        </div>
      </Popover>
    );
  }

  render() {
    const themeTemplate = (
      <div style={{ height: '30px', float: 'left' }}>
        {t('theme:')} &nbsp;
        <select onChange={this.onThemeChanged.bind(this)} value={this.state.gridTheme}>
          <option value="ag-blue">blue</option>
          <option value="ag-bootstrap">bootstrap</option>
          <option value="ag-dark">dark</option>
          <option value="ag-fresh">fresh</option>
        </select>
      </div>
    );

    const pageSizeTemplate = (
      <div style={{ height: '30px', marginLeft: '20px', float: 'left' }}>
        {t('page size:')} &nbsp;
        <select
          onChange={this.onPageSizeChanged.bind(this)}
          value={this.state.pageSize}
        >
          <option value="15">15</option>
          <option value="30">30</option>
          <option value="50">50</option>
          <option value="100">100</option>
          <option value="100000000">{t('all')}</option>
        </select>
      </div>
    );

    const filterTemplate = (
      <div style={{ height: '30px', marginLeft: '20px', float: 'left' }}>
        {t('filters:')}&nbsp;
        <input
          type="text"
          onChange={this.onQuickFilterText.bind(this)}
          placeholder="" style={{ height: '22px' }}
        />
      </div>
    );

    const exportTemplate = (
      <div style={{ height: '30px', float: 'left' }}>
        <button style={{ marginLeft: '20px' }} onClick={this.exportCsv.bind(this)}>
          {t('export_csv')}
        </button>
        <button style={{ marginLeft: '20px' }} onClick={this.exportExcel.bind(this)}>
          {t('export_excel')}
        </button>
      </div>
    );

    const gridTemplate = (
      <div
        style={{ height: this.props.height - 40, width: '100%', textAlign: 'left' }}
        className={this.state.gridTheme}
      >
        <AgGridReact
          // binding to simple properties
          showToolPanel={this.state.showToolPanel}
          quickFilterText={this.state.quickFilterText}
          // group properties
          suppressRowClickSelection="false"
          groupDefaultExpanded="1"
          groupIncludeFooter="true"
          groupUseEntireRow="false"
          rowSelection="multiple"
          enableColResize="true"      // 列大小调整
          enableSorting="true"        // 排序
          enableFilter="true"         // 筛选
          groupHeaders="true"         // 列groupby header
          rowHeight="22"              // 行高
          // debug="true"
          enableStatusBar="true"      // 状态
          enableRangeSelection="true" // 多选
          groupIncludeFooter="true"   // footer
          // rowModelType={this.props.form_data.hide_options == false ? "pagination" : "infinite"}
          suppressAutoSize="true"
          //remove filter
          //suppressMenuFilterPanel='true'
          //suppressMenuMainPanel='true'
          //suppressMenuColumnPanel='true'
          //suppressContextMenu='true'

          // all values as React props
          gridOptions={this.gridOptions}

          // listening for events
          onGridReady={this.onGridReady.bind(this)}
        />
      </div>
    );

    return (
      <div>
        {this.props.form_data.hide_options &&
          <div>
            {gridTemplate}
          </div>
        }
        {!this.props.form_data.hide_options &&
          <div>
            <div style={{ marginTop: '2px', overflow: 'hidden' }}>
              {themeTemplate}
              {pageSizeTemplate}
              {filterTemplate}
              {exportTemplate}
            </div>
            {gridTemplate}
          </div>
        }
      </div>
    );
  }
}
AgGrid.propTypes = propTypes;

function agGridVis(slice, payload) {

  slice.container.html('');
  ReactDOM.render(
    <AgGrid
      form_data={slice.formData}
      data={payload.data}
      height={slice.height()}
      slice={slice}
    />,
    document.getElementById(slice.containerId)
  );
}

module.exports = agGridVis;
