import React from 'react';
import { Table, Icon, Button, Modal, Row, Col, Input, Switch, Select } from 'antd';
import Add from './Add';
import Modify from './Modify';

import { t } from '../../locales';

const $ = window.$ = require('jquery');
const { TextArea } = Input;

const propTypes = {
  model: React.PropTypes.string.isRequired,
  params: React.PropTypes.object.isRequired,
};

export default class List extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      columns: null,
      dataSource: null,
      showVisible: false,
      showInfo: null,

      editVisible: false,
      editInfo: null,
      modifyObj: {},

      addVisible: false,
      addInfo: null,
      newObj: {},

      showTables: false,
      tables: [],
    };
  }

  componentWillMount() {
    this.loadTable();
  }

  loadTable() {
    const _this = this;
    $.get(`/${this.props.model.toLowerCase()}/api/read`, this.props.params, function (data) {
      // set columns
      const list_columns = data.list_columns.map(column => {
        return {
          title: column,
          dataIndex: column,
          key: column,
          render: (text, record) => {
            text = text === null ? '' : text.toString();
            if (text.startsWith('<a')) {
              if (column === 'creator' || column === 'changed_by_' ) {
                return $(text).html();
              } else {
                // add standalone on links
                let url = $(text).attr('href');
                if (url.startsWith('/superset/explore')){
                  if (url.indexOf('?') != -1) {
                    url += '&hideNav=true';
                  } else {
                    url += '?hideNav=true';
                  }
                } else {
                  if (url.indexOf('?') != -1)  {
                    url += '&standalone=true';
                  } else {
                    url += '?standalone=true';
                  }
                }
                return <a href={url}>{$(text).html()}</a>;
              }
            } else if (text.startsWith('<')) {
              return $(text).html();
            }
            return text;
          },
        }
      });

      // add operate
      list_columns.push({
        title: 'operate',
        dataIndex: 'operate',
        key: 'operate',
        render: (text, record) => {
          return  (
            <div className="btn-group btn-group-xs">    
              <a className="btn btn-sm btn-default" onClick={_this.showModal.bind(_this, record.id)} style={{ marginRight: 5 }}>
                  <i className="fa fa-search"></i>
              </a>  
              <a className="btn btn-sm btn-default" onClick={_this.editModal.bind(_this, record.id)} style={{ marginRight: 5 }}>
                  <i className="fa fa-edit"></i>
              </a>
              <a className="btn btn-sm btn-default" onClick={_this.del.bind(_this, record.id)}>
                  <i className="fa fa-eraser"></i>
              </a>
            </div>
          );
        },
      })

      // set datasource
      const r = [];
      data.result.map((item, index) => {
        item['id'] = data.pks[index];
        r.push(item);
      });
      _this.setState({
        columns: list_columns,
        dataSource: r,
      })
    });
  }

  // show detail modal
  showModal(id) {
    const _this = this;
    $.get(`/${this.props.model.toLowerCase()}/api/get/${id}`, function (data) {
      _this.setState({
        showInfo: data,
        showVisible: true,
      });
    });
  }

  onCancel(type) {
    if (type === 'show') {
      this.setState({
        showInfo: null,
        showVisible: false,
      });
    } else if (type === 'modify') {
      this.setState({
        editInfo: null,
        editVisible: false,
      });
    } else if (type === 'add') {
      this.setState({
        addInfo: null,
        addVisible: false,
      });
    }
  }

  onSuccess(type) {
    if (type === 'modify') {
      this.setState({
        editInfo: null,
        editVisible: false,
      });
      
    } else if (type === 'add') {
      this.setState({
        addInfo: null,
        addVisible: false,
      });
    }
    this.loadTable();
  }

  // show edit modal
  editModal(id) {
    const _this = this;
    $.get(`/hand/${_this.props.model}/getColumns/edit`, function(editColumns) {
      $.get(`/${_this.props.model.toLowerCase()}/api/get/${id}`, function (data) {
        data['edit_columns'] = JSON.parse(editColumns);
        // init new obj
        const modifyObj = {};
        data['edit_columns'].map(obj => {
            const key = obj.column;
            modifyObj[key] = data.result[key] === 'None' ? null : data.result[key];
        });
        _this.setState({
          modifyObj: modifyObj,
          editInfo: data,
          editVisible: true,
          showTables: false,
          tables: [],
        });
      });
    });
  }

  renderCascade(info, column, operate) {
    let mode = 'multiple';
    let url;
    if (column === 'dashboards') {
      url = '/hand/explore/getDashboards';
    } else if (column === 'slices') {
      url = '/hand/explore/getSlices';
    } else if (column === 'table') {
      url = '/hand/explore/getTables';
      // single select
      mode = '';
    } else if (column === 'database') {
      url = '/hand/explore/getDatabases';
      // single select
      mode = '';
    }
    let defaultValue = [];
    let options = [];
    let obj = {};

    $.ajax({
      type: 'GET',
      url: url,
      async: false,
      success: function(data) {
        obj = JSON.parse(data);
        // set options
        options = Object.keys(obj).map(id => {
          return (
            <Select.Option key={id}>{obj[id]}</Select.Option>
          );
        });
      },
      error: function(xhr) {
        alert(xhr.responseText)
      }
    });

    if (operate === 'modify') {
      // set default value
      const value = info.result[column];
      if (column === 'database' || column === 'table') {
        Object.keys(obj).map(id => {
          if (obj[id] == value) {
            defaultValue = id;
          }
        });
      } else {
        const array = value.substring(1, value.length-1).split(', ');
        Object.keys(obj).map(id => {
          if (array.indexOf(obj[id]) !== -1) {
            defaultValue.push(id + '');
          }
        });
      }
    }
    this.state.modifyObj[column] = defaultValue;
    return (
      <Select
        id={column}
        mode={mode}
        style={{ width: '100%' }}
        placeholder={t('Please Select')}
        defaultValue={defaultValue}
        onChange={this.handleChange.bind(this, "CASCADE", column, operate)}
      >
        {options}
      </Select>
    )
  }

  handleChange(fieldType, column, operate, event) {
    let value;
    if (fieldType.startsWith('TEXT') || fieldType.startsWith('VARCHAR') || fieldType.startsWith('INTEGER')) {
      value = event.target.value;
    } else if (fieldType.startsWith('BOOLEAN') || fieldType.startsWith('CASCADE')) {
      value = event;
    }
    if (operate === 'modify') {
      this.state.modifyObj[column] = value;
    } else {
      this.state.newObj[column] = value;
    }
  } 

  // show add modal
  addModal() {
    const _this = this;
    if (this.props.model !== 'SliceModelView') {
      $.get(`/hand/${_this.props.model}/getColumns/add`, function(addColumns) {
        $.get(`/${_this.props.model.toLowerCase()}/api`, function (api) {
          const data = {};
          data['add_columns'] = JSON.parse(addColumns);
          data['label_columns'] = api.label_columns;
          _this.setState({
            addInfo: data,
            addVisible: true,
            showTables: false,
          });
        });
      });
    } else {
      _this.setState({
        addInfo: 'slice',
        addVisible: true,
        showTables: false,
      });
    }
  }

  del(id) {
    const _this = this;
    Modal.confirm({
      title: 'Do you Want to delete this item?',
      content: '',
      onOk() {
        $.ajax({
          type: 'DELETE',
          url: `/${_this.props.model.toLowerCase()}/api/delete/${id}`,
          dataType: 'json',
          success: function(result) {
            Modal.success({
              title: '',
              content: t('Delete Success!'),
              onOk: function() {
                _this.loadTable();
              }
            });
          },
          error: function(xhr, error) {
             Modal.error({
              title: t('Update Failed'),
              content: JSON.stringify(JSON.parse(xhr.responseText).error_details),
            });
          }
        });
      },
      onCancel() {
        console.log('Cancel');
      },
    });
  }

  testConnection(type) {
    let obj, data;
    if (type === 'modify') {
      obj = this.state.modifyObj;
    } else {
      obj = this.state.newObj;
    }
    try {
      data = JSON.stringify({
        uri: obj.sqlalchemy_uri,
        name: obj.database_name,
        extras: JSON.parse(obj.extra),
      });
    } catch (err) {
      Modal.error({
        'title': '',
        'content': err.toString(),
      });
      return;
    }
    const _this = this;
    $.ajax({
      type: 'POST',
      url: '/superset/testconn',
      data: data,
      dataType: 'json',
      contentType: 'application/json; charset=utf-8',
      success: function(result) {
        Modal.success({
          title: '',
          content: t('Seems Ok!'),
          onOk: function() {
            _this.setState({
              showTables: true,
              tables: result,
            });
          }
        });
      },
      error: function(xhr) {
        Modal.error({
          title: '',
          content: xhr.responseText,
        });
      }
    });
  }

  render() {
    return (
      <div style={{ width: '98%' }}>
        <Button
          type="primary"
          style={{ margin: '10px 0px 10px 20px' }}
          onClick={this.addModal.bind(this)}
        >
          {t('Add Record')}
        </Button>
        <Table
          style={{ marginLeft: 20 }}
          size='small'
          bordered
          columns={this.state.columns}
          dataSource={this.state.dataSource}
        />
        {this.state.showInfo !== null && 
          <Modal
            width={'80%'}
            style={{ top: 20 }}
            title={this.props.model}
            visible={this.state.showVisible}
            onCancel={this.onCancel.bind(this, 'show')}
            footer={[
              <span></span>
            ]}
          >
            {this.state.showInfo.include_columns.map(key => {
              return (
                <Row style={{ marginBottom: 5 }}>
                  <Col span={4}>{this.state.showInfo.label_columns[key] || key}</Col>
                  <Col span={20}>{this.state.showInfo.result[key].toString()}</Col>
                </Row>
              )
            })}
          </Modal>
        }
        {this.state.editInfo !== null && 
          <Modify
            model={this.props.model}
            editVisible={this.state.editVisible}
            editInfo={this.state.editInfo}
            modifyObj={this.state.modifyObj}
            onCancel={this.onCancel.bind(this)}
            onSuccess={this.onSuccess.bind(this)}
            handleChange={this.handleChange.bind(this)}
            renderCascade={this.renderCascade.bind(this)}
            // testConn
            showTables={this.state.showTables}
            tables={this.state.tables}
            testConnection={this.testConnection.bind(this)}
          />
        }
        {this.state.addInfo !== null &&
          <Add
            model={this.props.model}
            addVisible={this.state.addVisible}
            addInfo={this.state.addInfo}
            newObj={this.state.newObj}
            onCancel={this.onCancel.bind(this)}
            onSuccess={this.onSuccess.bind(this)}
            handleChange={this.handleChange.bind(this)}
            renderCascade={this.renderCascade.bind(this)}
            // testConn
            showTables={this.state.showTables}
            tables={this.state.tables}
            testConnection={this.testConnection.bind(this)}
          />
        }
      </div>
    );
  }
}

List.propTypes = propTypes;
