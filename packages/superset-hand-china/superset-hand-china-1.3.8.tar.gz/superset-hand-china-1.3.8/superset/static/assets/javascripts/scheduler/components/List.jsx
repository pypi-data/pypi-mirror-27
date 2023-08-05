import React from 'react';
import { Table, Icon, Button, Modal, Popconfirm } from 'antd';

import { t } from '../../locales';

const $ = window.$ = require('jquery');

const propTypes = {
  form_data: React.PropTypes.object.isRequired,
};

export default class List extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      showSchedulerLog: false,
      log_datasources: null,
    };
  }

  parseExpr(s) {
    if (s.mode === 'interval') {
      return s.interval_expr;
    } else if (s.mode === 'date') {
      return "run_date='" + s.date_run_date + "'";
    }
    // cron
    let str = '';
    if (s.cron_year != null) {
      str += "year='" + s.cron_year + "',";
    }
    if (s.cron_month != null) {
      str += "month='" + s.cron_month + "',";
    }
    if (s.cron_day != null) {
      str += "day='" + s.cron_day + "',";
    }
    if (s.cron_week != null) {
      str += "week='" + s.cron_week + "',";
    }
    if (s.cron_day_of_week != null) {
      str += "day_of_week='" + s.cron_day_of_week + "',";
    }
    if (s.cron_hour != null) {
      str += "hour='" + s.cron_hour + "',";
    }
    if (s.cron_minute != null) {
      str += "minute='" + s.cron_minute + "',";
    }
    if (s.cron_second != null) {
      str += "second='" + s.cron_second + "',";
    }
    return str.substring(0, str.length - 1);
  }

  addScheduler() {
    location.href = '/hand/schedulers/add/1';
  }

  modifyScheduler(id) {
    location.href = '/hand/schedulers/modify/' + id;
  }

  operateJob(id, operate) {
    if (operate === 'delete') {
      const _this = this;
      Modal.confirm({
        title: t('Do you want to delete this scheduler?'),
        onOk() {
          _this.operate(id, operate);
        },
        onCancel() {
          return;
        },
      });
    } else {
      this.operate(id, operate);
    }
    
  }

  operate(id, operate) {
    $.ajax({
      type: 'get',
      url: '/hand/job/' + operate + '/' + id,
      dataType: 'json',
      success: function (data) {
        let operate1;
        if(operate === 'active'){
          operate1 = t('active');
        } else if(operate === 'delete'){
          operate1 = t('delete');
        } else if(operate === 'resume'){
          operate1 = t('resume');
        } else if(operate === 'pause'){
          operate1 = t('pause');
        }
        if (data) {
          Modal.success({
            title: operate1 + t(' success'),
            onOk() {
              location.href = '/hand/schedulers/list/1';
            }
          });
        } else {
          Modal.error({
            title: operate1 + t(' failed'),
          });
        }
      },
      error: function () {
        Modal.error({
          title: t('Unknown Error'),
        });
      },
    });
  }

  showSchedulerLog(schedulerId) {
    const _this = this;
    $.get(`/hand/getSchedulerLog/${schedulerId}`, function(data) {
      _this.setState({
        log_datasources: data,
        showSchedulerLog: true,
      });
    });
  }

  onCancel() {
    this.setState({
      showSchedulerLog: false,
    });
  }

  render() {
    const columns = [{
      title: t('Description'),
      dataIndex: 'description',
      key: 'description',
      render: (text, record) => {
        return (<a href={'/hand/schedulers/modify/' + record.id}>{text}</a>);
      },
    }, {
      title: t('Mode'),
      dataIndex: 'mode',
      key: 'mode',
    }, {
      title: t('Expression'),
      dataIndex: 'expression',
      key: 'expression',
      render: (text, record) => { return this.parseExpr(record); }
    }, {
      title: t('Start_date'),
      dataIndex: 'start_date',
      key: 'start_date',
    }, {
      title: t('End_date'),
      dataIndex: 'end_date',
      key: 'end_date',
    }, {
      title: t('Is_active'),
      dataIndex: 'is_active',
      key: 'is_active',
      render: (text, record) => {
        return text ? <span style={{ color: 'green' }}>{t('true')}</span> : 
        (
          <Button
            type="primary"
            style={{  backgroundColor: '#37a14a' }}
            onClick={this.operateJob.bind(this, record.id, 'active')}
          >
            {t('active')}
          </Button>
        )
      }
    }, {
      title: t('Is_running'),
      dataIndex: 'is_running',
      key: 'is_running',
      render: (text, record) => {
        if (record.mode !== 'date'
            || (record.mode === 'date' && new Date().getTime() < new Date(record.date_run_date).getTime())
        ) {
          if (!record.is_active) {
            return (
              <div>
                <Button disabled="disabled">{t('Stop')}</Button>
                <Button disabled="disabled" style={{ marginLeft: '20px' }}>{t('Start')}</Button>
              </div>
            );
          }
          if (text) {
            return (
              <div>
                <Button
                  type="danger"
                  style={{ background: 'red', color: 'white' }}
                  onClick={this.operateJob.bind(this, record.id, 'pause')}
                >
                  {t('Stop')}
                </Button>
                <Button disabled="disabled" style={{ marginLeft: '20px' }}>{t('Start')}</Button>
              </div>
            );
          } else {
            return (
              <div>
                <Button disabled="disabled">{t('Stop')}</Button>
                <Button
                  type="primary"
                  style={{ marginLeft: '20px', backgroundColor: '#00A699' }}
                  onClick={this.operateJob.bind(this, record.id, 'resume')}
                >
                  {t('Start')}
                </Button>
              </div>
            );
          }
        } else {
          // the date scheduler has started
          return (
            <div>
              <Button disabled="disabled">{t('Stop')}</Button>
              <Button disabled="disabled" style={{ marginLeft: '20px' }}>{t('Start')}</Button>
            </div>
          );
        }
      }
    }, {
      title: t('Actions'),
      dataIndex: 'actions',
      key: 'actions',
      render: (text, record) => {
        return (
          <div>
            <Button
              type="primary"
              onClick={this.modifyScheduler.bind(this, record.id)}
            >
              {t('Modify')}
            </Button>
            <Button
              type="danger"
              style={{ marginLeft: '20px', background: 'red', color: 'white' }}
              onClick={this.operateJob.bind(this, record.id, 'delete')}
            >
              {t('Delete')}
            </Button>
            <Button
              type="primary"
              style={{ marginLeft: '20px' }}
              onClick={this.showSchedulerLog.bind(this, record.id)}
            >
              {t('Send Mail Log')}
            </Button>
          </div>
        );
      }
    }];

    const log_columns = [{
      title: t('Subject'),
      dataIndex: 'subject',
      key: 'subject',
      render: (text, record) => {
        return text;
      }
    }, {
      title: t('Sender'),
      dataIndex: 'sender',
      key: 'sender',
      render: (text, record) => {
        return text;
      }
    }, {
      title: t('Receiver'),
      dataIndex: 'receiver',
      key: 'receiver',
      render: (text, record) => {
        return text;
      }
    }, {
      title: t('Status'),
      dataIndex: 'status',
      key: 'status',
      render: (text, record) => {
        if (record.status) {
          return <span style={{ color: 'green' }}>{t('Success')}</span>;
        } else {
          return (
            <div>
              <span style={{ color: 'red', marginRight: 20 }}>{t('Fail')}</span>
              <Popconfirm placement="bottom" title={record.reason}>
                <a>{t('Detail')}</a>
              </Popconfirm>
            </div>
          )
        }
      }
    }, {
      title: t('Created_on'),
      dataIndex: 'created_on',
      key: 'created_on',
      render: (text, record) => {
        return text;
      }
    }];

    return (
      <div style={{ width: '98%' }}>
        <Button
          type="primary"
          style={{ marginLeft: 20, marginBottom: 10, backgroundColor: '#00A699' }}
          onClick={this.addScheduler.bind(this)}
        >
          {t('Add Schedule')}
        </Button>
        <Table
          style={{ marginLeft: 20 }}
          size='small'
          columns={columns}
          dataSource={this.props.form_data.schedulers}
        />
        <Modal
          width={'80%'}
          style={{ top: 20 }}
          title={t('Mail Log')}
          visible={this.state.showSchedulerLog}
          onCancel={this.onCancel.bind(this)}
          footer={[]}
        >
          <Table
            style={{ marginLeft: 20 }}
            size='small'
            columns={log_columns}
            dataSource={this.state.log_datasources}
          />
        </Modal>

      </div>
    );
  }
}

List.propTypes = propTypes;
