import React from 'react';
import PropTypes from 'prop-types';

import Controls from './Controls';
import EditableTitle from '../../components/EditableTitle';
import { t } from '../../locales';

const propTypes = {
  dashboard: PropTypes.object,
};
const defaultProps = {
};

class Header extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      showTitle: true,
      showContorl: true,
    };
    this.handleSaveTitle = this.handleSaveTitle.bind(this);
  }
  componentWillMount() {
    if (this.getQueryString('isTitle') === 'false') {
      this.setState({
        showTitle: false,
        showContorl: false,
      });
    }
  }
  // get url param
  getQueryString(name) {
    const reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    const r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]);
    return null;
  }
  handleSaveTitle(title) {
    this.props.dashboard.updateDashboardTitle(title);
  }
  render() {
    const dashboard = this.props.dashboard;
    return (
      <div className="title">
        {this.state.showTitle &&
          <div className="pull-left">
            <h1 className="outer-container">
              <EditableTitle
                title={dashboard.dashboard_title}
                canEdit={dashboard.dash_save_perm}
                onSaveTitle={this.handleSaveTitle}
                showHeaderModal="Dashboard"
                noPermitTooltip={t('You don\'t have the rights to alter this dashboard.')}
              />
              <span is class="favstar" class_name="Dashboard" obj_id={dashboard.id} />
            </h1>
          </div>
        }
        {this.state.showContorl &&
          <div className="pull-right" style={{ marginTop: '35px' }}>
            <Controls dashboard={dashboard} />
          </div>
        }
        <div className="clearfix" />
      </div>
    );
  }
}
Header.propTypes = propTypes;
Header.defaultProps = defaultProps;

export default Header;
