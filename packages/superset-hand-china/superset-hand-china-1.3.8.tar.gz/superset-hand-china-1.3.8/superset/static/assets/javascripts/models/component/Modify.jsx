import React from 'react';
import { Table, Icon, Button, Modal, Row, Col, Input, Switch, Select, Tabs } from 'antd';
import List from './List';

import { t } from '../../locales';

const $ = window.$ = require('jquery');
const { TextArea } = Input;
const TabPane = Tabs.TabPane;

const propTypes = {
  model: React.PropTypes.string.isRequired,
  editVisible: React.PropTypes.string.isRequired,
  editInfo: React.PropTypes.string.isRequired,
  modifyObj: React.PropTypes.string.isRequired,
  onCancel: React.PropTypes.func.isRequired,
  onSuccess: React.PropTypes.func.isRequired,
  handleChange: React.PropTypes.func.isRequired,
  renderCascade: React.PropTypes.func.isRequired,
  showTables: React.PropTypes.bool.isRequired,
  tables: React.PropTypes.array.isRequired,
  testConnection: React.PropTypes.func.isRequired
};

export default class Add extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      mode: 'modify',
      activeKey: '1',
    }
  }

  modify(editInfo) {
    const _this = this;
    $.ajax({
      type: 'PUT',
      url: `/${this.props.model.toLowerCase()}/api/update/${editInfo.pk}`,
      data: this.props.modifyObj,
      dataType: 'json',
      success: function(result) {
        // update cascade table
        if (_this.props.model === 'DashboardModelView') {
          _this.updateDashboardSlices('dashboard', editInfo.pk);
        } else if (_this.props.model === 'SliceModelView') {
          _this.updateDashboardSlices('slice', editInfo.pk);
        } else {
          Modal.success({
            title: '',
            content: t('Update Success!'),
            onOk: function() {
              _this.onSuccess();
            }
          });
        }
      },
      error: function(xhr) {
        Modal.error({
          title: '',
          content: t('Update Failed'),
        });
      }
    });
  }

  // update dashboard_slices table
  updateDashboardSlices(type, id) {
    const _this = this;
    let data = {};
    if (type === 'dashboard') {
      if (this.props.modifyObj.slices !== undefined) {
        data = {
          dashboard_id: id,
          slices: this.props.modifyObj.slices.join(','),
          type: type,
        };
      }
    } else if (type === 'slice') {
      data = {
        slice_id: id,
        dashboards: this.props.modifyObj.dashboards.join(','),
        type: type,
      };
    }
    $.ajax({
      type: 'POST',
      url: '/hand/updateDashboardSlices',
      data: data,
      success: function(result) {
        Modal.success({
          title: '',
          content: t('Update Success!'),
          onOk: function() {
            _this.onSuccess();
          }
        });
      },
      error: function(xhr) {
        Modal.error({
          title: '',
          content: t('Update Failed'),
        });
      }
    });
  }

  onCancel() {
    this.props.onCancel(this.state.mode);
  }

  handleChange(type, column, event) {
    this.props.handleChange(type, column, this.state.mode, event);
  }

  renderCascade(info, column) {
    return this.props.renderCascade(info, column, this.state.mode);
  }

  onSuccess() {
    this.props.onSuccess(this.state.mode);
  }

  testConnection() {
    this.props.testConnection(this.state.mode);
  }

  renderColumns() {
    return this.props.editInfo.edit_columns.map(obj => {
      const key = obj.column;
      const type = obj.type;
      const info = this.props.editInfo;
      return (
        <Row style={{ marginBottom: 5 }}>
          <Col span={4}>{info.label_columns[key] || key}</Col>
          <Col span={20}>
            {(type.startsWith('VARCHAR') || type.startsWith('INTEGER')) &&
              <div>
                <Input
                  id={key}
                  placeholder={info.label_columns[key] || key}
                  defaultValue={info.result[key] == 'None' ? null : info.result[key]}
                  onChange={this.handleChange.bind(this, type, key)}
                />
                {key === 'sqlalchemy_uri' &&
                  <Button
                    type="primary"
                    style={{ marginTop: 5 }}
                    onClick={this.testConnection.bind(this)}
                  >
                    {t('Test Connection')}
                  </Button>
                }
              </div>
            }
            {(type.startsWith('TEXT')) &&
              <TextArea
                id={key}
                placeholder={info.label_columns[key] || key}
                defaultValue={info.result[key] == 'None' ? null : info.result[key]}
                rows={4}
                onChange={this.handleChange.bind(this, type, key)}
              />
            }
            {(type.startsWith('BOOLEAN')) &&
              <Switch
                id={key}
                defaultChecked={info.result[key]}
                onChange={this.handleChange.bind(this, type, key)}
              />
            }
            {(type.startsWith('CASCADE')) &&
              this.renderCascade(info, key)
            }
          </Col>
        </Row>
      )
    });
  }

  callback(key) {
    this.setState({ activeKey: key });
  }

  render() {
    return (
      <Modal
        width={'80%'}
        style={{ top: 20 }}
        title={this.props.model}
        visible={this.props.editVisible}
        onCancel={this.onCancel.bind(this)}
        footer={[
          <Button key="submit" type="primary" size="large"
            onClick={this.modify.bind(this, this.props.editInfo)}
            style={{ display: this.state.activeKey === '1' ? '' : 'none' }}>
            {t('Modify')}
          </Button>,
        ]}
      >
        {this.props.model === 'TableModelView' &&
          <Tabs defaultActiveKey="1" onChange={this.callback.bind(this)} type="card">
            <TabPane tab="Detail" key="1">
              {this.renderColumns()}
            </TabPane>
            <TabPane tab="Sql Columns" key="2">
              <List model="TableColumnInlineView" params={{_flt_0_table_id: this.props.editInfo.pk}}/>
            </TabPane>
            <TabPane tab="Sql Metrics" key="3">
              <List model="SqlMetricInlineView" params={{_flt_0_table_id: this.props.editInfo.pk}}/>
            </TabPane>
          </Tabs>
        }
        {this.props.model !== 'TableModelView' &&
          this.renderColumns()
        }
        <div style={{ display: this.props.showTables ? 'block' : 'none', marginTop: 20 }}>
          <span style={{ marginLeft: 10, marginRight: 10 }}>{t('Tables:')}</span>
          {this.props.tables.map(xt => (<Button style={{ margin: '3px 5px 3px 5px' }}>{xt}</Button>))}
        </div>
      </Modal>
    )
  }
}