import React from 'react';
import { Table, Icon, Button, Modal, Row, Col, Input, Switch, Select } from 'antd';

import { t } from '../../locales';

const $ = window.$ = require('jquery');
const { TextArea } = Input;

const propTypes = {
  model: React.PropTypes.string.isRequired,
  addVisible: React.PropTypes.string.isRequired,
  addInfo: React.PropTypes.string.isRequired,
  newObj: React.PropTypes.string.isRequired,
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
      mode: 'add',
    }
  }

  add() {
    const _this = this;
    $.ajax({
      type: 'POST',
      url: `/${this.props.model.toLowerCase()}/api/create`,
      data: this.props.newObj,
      dataType: 'json',
      success: function(result) {
        // add cascade table
        if (_this.props.model === 'DashboardModelView') {
          _this.updateDashboardSlices('dashboard');
        } else if (_this.props.model === 'SliceModelView') {
          _this.updateDashboardSlices('slice');
        } else {
          Modal.success({
            title: '',
            content: t('Add Success!'),
            onOk: function() {
              _this.onSuccess();
            }
          });
        }
      },
      error: function(xhr) {
        // console.info(xhr);
        Modal.error({
          title: '',
          content: t('Add Failed'),
        });
      }
    });
  }

  // update dashboard_slices table
  updateDashboardSlices(type) {
    const _this = this;
    let data = {};
    if (type === 'dashboard') {
      // console.info(this.props.newObj.slices)
      if (this.props.newObj.slices !== undefined) {
        data = {
          dashboard_title: this.props.newObj.dashboard_title,
          slices: this.props.newObj.slices.join(','),
          type: type,
        };
      }
    } else if (type === 'slice') {
      data = {
        slice_name: this.props.newObj.slice_name,
        dashboards: this.props.newObj.dashboards.join(','),
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
          content: t('Add Success!'),
          onOk: function() {
            _this.onSuccess();
          }
        });
      },
      error: function(xhr) {
        Modal.error({
          title: '',
          content: t('Add Failed'),
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

  render() {
    return (
      <Modal
        width={'80%'}
        style={{ top: 20 }}
        title={this.props.model}
        visible={this.props.addVisible}
        onCancel={this.onCancel.bind(this)}
        footer={[
            <Button key="submit" type="primary" size="large" onClick={this.add.bind(this)}
                    style={{ display: this.props.model === 'SliceModelView' ? 'none' : '' }}>
              {t('Add')}
            </Button>,
        ]}
      >
        {this.props.model !== 'SliceModelView' && this.props.addInfo.add_columns.map(obj => {
          const key = obj.column;
          const type = obj.type;
          const info = this.props.addInfo;
          return (
            <Row style={{ marginBottom: 5 }}>
              <Col span={4}>{info.label_columns[key] || key}</Col>
              <Col span={20}>
                {(type.startsWith('VARCHAR') || type.startsWith('INTEGER')) &&
                  <div>
                    <Input
                      id={key}
                      placeholder={info.label_columns[key] || key}
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
                      rows={4}
                      onChange={this.handleChange.bind(this, type, key)}
                    />
                }
                {(type.startsWith('BOOLEAN')) &&
                  <Switch
                    id={key}
                    onChange={this.handleChange.bind(this, type, key)}
                  />
                }
                {(type.startsWith('CASCADE')) &&
                  this.renderCascade(info, key)
                }
              </Col>
            </Row>
          )
        })}
      
      <div style={{ display: this.props.showTables ? 'block' : 'none', marginTop: 20 }}>
        <span style={{ marginLeft: 10, marginRight: 10 }}>{t('Tables:')}</span>
        {this.props.tables.map(xt => (<Button style={{ margin: '3px 5px 3px 5px' }}>{xt}</Button>))}
      </div>

        {this.props.model === 'SliceModelView' &&
          <div>
            <iframe
              src='/slicemodelview/add?standalone=true'
              style={{width: '100%', height: '50%', border: '0px'}}
            />
          </div>
        }
      </Modal>
    )
  }
}
