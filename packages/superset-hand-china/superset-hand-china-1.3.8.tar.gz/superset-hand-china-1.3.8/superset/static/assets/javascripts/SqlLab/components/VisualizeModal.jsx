/* global notify */
import moment from 'moment';
import React from 'react';
import PropTypes from 'prop-types';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { Alert, Button, Col, Modal } from 'react-bootstrap';

import Select from 'react-select';
import { Table } from 'reactable';
import shortid from 'shortid';
import { getExploreUrl } from '../../explore/exploreUtils';
import * as actions from '../actions';
import { VISUALIZE_VALIDATION_ERRORS } from '../constants';
import visTypes from '../../explore/stores/visTypes';
import { t } from '../../locales';

const CHART_TYPES = Object.keys(visTypes)
  .filter(typeName => !!visTypes[typeName].showOnExplore)
  .map((typeName) => {
    const vis = visTypes[typeName];
    return {
      value: typeName,
      label: vis.label,
      requiresTime: !!vis.requiresTime,
    };
  });

const propTypes = {
  actions: PropTypes.object.isRequired,
  onHide: PropTypes.func,
  query: PropTypes.object,
  show: PropTypes.bool,
  datasource: PropTypes.string,
  errorMessage: PropTypes.string,
  timeout: PropTypes.number,
};
const defaultProps = {
  show: false,
  query: {},
  onHide: () => {},
};

class VisualizeModal extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      chartType: CHART_TYPES[0],
      modalShow: false,
      datasourceName: this.datasourceName(),
      columns: this.getColumnFromProps(),
      hints: [],
    };
  }
  componentDidMount() {
    this.validate();
  }
  getColumnFromProps() {
    const props = this.props;
    if (!props ||
        !props.query ||
        !props.query.results ||
        !props.query.results.columns) {
      return {};
    }
    const columns = {};
    props.query.results.columns.forEach((col) => {
      columns[col.name] = col;
    });
    return columns;
  }
  datasourceName() {
    const { query } = this.props;
    const uniqueId = shortid.generate();
    let datasourceName = uniqueId;
    if (query) {
      datasourceName = query.user ? `${query.user}-` : '';
      datasourceName += query.db ? `${query.db}-` : '';
      datasourceName += `${query.tab}-${uniqueId}`;
    }
    return datasourceName;
  }
  validate() {
    const hints = [];
    const cols = this.mergedColumns();
    const re = /^\w+$/;
    Object.keys(cols).forEach((colName) => {
      if (!re.test(colName)) {
        hints.push(
          <div>
            {t('%s is not right as a column name, please alias it ' +
            '(as in SELECT count(*) ', colName)} <strong>{t('AS my_alias')}</strong>) {t('using only ' +
            'alphanumeric characters and underscores')}
          </div>);
      }
    });
    if (this.state.chartType === null) {
      hints.push(VISUALIZE_VALIDATION_ERRORS.REQUIRE_CHART_TYPE);
    } else if (this.state.chartType.requiresTime) {
      let hasTime = false;
      for (const colName in cols) {
        const col = cols[colName];
        if (col.hasOwnProperty('is_date') && col.is_date) {
          hasTime = true;
        }
      }
      if (!hasTime) {
        hints.push(VISUALIZE_VALIDATION_ERRORS.REQUIRE_TIME);
      }
    }
    this.setState({ hints });
  }
  changeChartType(option) {
    this.setState({ chartType: option }, this.validate);
  }
  mergedColumns() {
    const columns = Object.assign({}, this.state.columns);
    if (this.props.query && this.props.query.results.columns) {
      this.props.query.results.columns.forEach((col) => {
        if (columns[col.name] === undefined) {
          columns[col.name] = col;
        }
      });
    }
    return columns;
  }
  buildVizOptions() {
    return {
      chartType: this.state.chartType.value,
      datasourceName: this.state.datasourceName,
      columns: this.state.columns,
      sql: this.props.query.sql,
      dbId: this.props.query.dbId,
    };
  }
  buildVisualizeAdvise() {
    let advise;
    const timeout = this.props.timeout;
    const queryDuration = moment.duration(this.props.query.endDttm - this.props.query.startDttm);
    if (Math.round(queryDuration.asMilliseconds()) > timeout * 1000) {
      advise = (
        <Alert bsStyle="warning">
          {t('This query took ')} {Math.round(queryDuration.asSeconds())} {t('seconds to run,')}
          {t('and the explore view times out at ')} {timeout} {t(' seconds, ')}
          {t('following this flow will most likely lead to your query timing out.' +
          'We recommend your summarize your data further before following that flow.' +
          'If activated you can use the ')} <strong>CREATE TABLE AS</strong> {t('feature ' +
          'to store a summarized data set that you can then explore.')}
        </Alert>);
    }
    return advise;
  }
  checkDatasourceName() {
    const _this = this;
    const datasourceName = _this.state.datasourceName;
    $.ajax({
      type: 'get',
      url: '/hand/queryTableData',
      dataType: 'json',
      success: function (data) {
        _this.setState({ modalShow: false });
        for(let i = 0; i < data.length; i++) {
          if(datasourceName === data[i].table_name) {
            _this.setState({ modalShow: true});
          }
        }
        if(_this.state.modalShow === false) {
          _this.visualize();
        }
      },
      error: function (error) {
        console.info(error);
      },
    });
  }
  visualize() {
    const _this = this;
    this.props.actions.createDatasource(this.buildVizOptions(), this)
      .done(() => {
        const columns = Object.keys(this.state.columns).map(k => this.state.columns[k]);
        const mainGroupBy = columns.filter(d => d.is_dim)[0];
        const formData = {
          datasource: this.props.datasource,
          viz_type: this.state.chartType.value,
          since: '100 years ago',
          limit: '0',
        };
        if (mainGroupBy) {
          formData.groupby = [mainGroupBy.name];
        }
        notify.info(t('Creating a data source and popping a new tab'));
        _this.setState({ modalShow: false });
        window.open('/tablemodelview/list/');
      })
      .fail(() => {
        notify.error(this.props.errorMessage);
      });
  }
  changeDatasourceName(event) {
    this.setState({ datasourceName: event.target.value }, this.validate);
  }
  changeCheckbox(attr, columnName, event) {
    let columns = this.mergedColumns();
    const column = Object.assign({}, columns[columnName], { [attr]: event.target.checked });
    columns = Object.assign({}, columns, { [columnName]: column });
    this.setState({ columns }, this.validate);
  }
  changeAggFunction(columnName, option) {
    let columns = this.mergedColumns();
    const val = (option) ? option.value : null;
    const column = Object.assign({}, columns[columnName], { agg: val });
    columns = Object.assign({}, columns, { [columnName]: column });
    this.setState({ columns }, this.validate);
  }
  render() {
    if (!(this.props.query) || !(this.props.query.results) || !(this.props.query.results.columns)) {
      return (
        <div className="VisualizeModal">
          <Modal show={this.props.show} onHide={this.props.onHide}>
            <Modal.Body>
              {t('No results available for this query')}
            </Modal.Body>
          </Modal>
        </div>
      );
    }
    const tableData = this.props.query.results.columns.map(col => {
      const header = {};
      header[t('column')] = col.name;
      header[t('is_dimension')] = (
        <input
          type="checkbox"
          onChange={this.changeCheckbox.bind(this, 'is_dim', col.name)}
          checked={(this.state.columns[col.name]) ? this.state.columns[col.name].is_dim : false}
          className="form-control"
        />
      );
      header[t('is_date')] = (
        <input
          type="checkbox"
          className="form-control"
          onChange={this.changeCheckbox.bind(this, 'is_date', col.name)}
          checked={(this.state.columns[col.name]) ? this.state.columns[col.name].is_date : false}
        />
      );
      header[t('agg_func')] = (
        <Select
          options={[
            { value: 'sum', label: t('SUM(x)') },
            { value: 'min', label: t('MIN(x)') },
            { value: 'max', label: t('MAX(x)') },
            { value: 'avg', label: t('AVG(x)') },
            { value: 'count_distinct', label: t('COUNT(DISTINCT x)') },
          ]}
          onChange={this.changeAggFunction.bind(this, col.name)}
          value={(this.state.columns[col.name]) ? this.state.columns[col.name].agg : null}
        />
      );
      return header;
    });
    const alerts = this.state.hints.map((hint, i) => (
      <Alert bsStyle="warning" key={i}>{hint}</Alert>
    ));
    const modal = (
      <div className="VisualizeModal">
        <Modal show={this.props.show} onHide={this.props.onHide}>
          <Modal.Header closeButton>
            <Modal.Title>{t('Visualize')}</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            {alerts}
            {this.buildVisualizeAdvise()}
            <div className="row">
              <Col md={6}>
                {t('Datasource Name')}
                <input
                  type="text"
                  className="form-control input-sm"
                  placeholder={t('datasource name')}
                  onChange={this.changeDatasourceName.bind(this)}
                  value={this.state.datasourceName}
                />
              </Col>
            </div>
            <hr />
            <Table
              className="table table-condensed"
              columns={[t('column'), t('is_dimension'), t('is_date'), t('agg_func')]}
              data={tableData}
            />
            <Button
              // onClick={this.visualize.bind(this)}
              onClick={this.checkDatasourceName.bind(this)}
              bsStyle="primary"
              disabled={(this.state.hints.length > 0)}
            >
              {t('Visualize')}
            </Button>
            <Modal show={this.state.modalShow} onHide={() => this.setState({ modalShow: false})}>
              <Modal.Header>
                <Modal.Title>{t('Make Sure to save as')}</Modal.Title>
              </Modal.Header>
              <Modal.Body>
                {t('Datasource Name [%s] already exists, confirm to replace it.', this.state.datasourceName)}
              </Modal.Body>
              <Modal.Footer>
                <Button onClick={() => this.setState({ modalShow: false})}>{t('Cancel')}</Button>
                <Button
                  onClick={this.visualize.bind(this)}
                  bsStyle="primary"
                >
                  {t('OK')}
                </Button>
              </Modal.Footer>
            </Modal>
          </Modal.Body>
        </Modal>
      </div>
    );
    return modal;
  }
}
VisualizeModal.propTypes = propTypes;
VisualizeModal.defaultProps = defaultProps;

function mapStateToProps(state) {
  return {
    datasource: state.datasource,
    errorMessage: state.errorMessage,
    timeout: state.common ? state.common.SUPERSET_WEBSERVER_TIMEOUT : null,
  };
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(actions, dispatch),
  };
}

export { VisualizeModal };
export default connect(mapStateToProps, mapDispatchToProps)(VisualizeModal);
