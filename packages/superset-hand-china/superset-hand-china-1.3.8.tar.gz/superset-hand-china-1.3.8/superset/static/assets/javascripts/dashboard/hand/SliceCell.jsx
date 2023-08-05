/* eslint-disable react/no-danger */
import React from 'react';
import PropTypes from 'prop-types';
import { t } from '../../locales';
import MenuType from './MenuType';

const propTypes = {
  slice: PropTypes.object.isRequired,
  removeSlice: PropTypes.func.isRequired,
  expandedSlices: PropTypes.object,
  index: PropTypes.number.isRequired,
};

function GetRequest() {
  const url = location.search; //获取url中"?"符后的字串 
  let theRequest = new Object();
  if(url.indexOf("?") != -1) {
    const str = url.substr(1);
    const strs = str.split("&");
    for(var i = 0; i < strs.length; i++) {
      theRequest[strs[i].split("=")[0]] = unescape(strs[i].split("=")[1]);
    }
  }
  return theRequest;
}



function SliceCell({ expandedSlices, removeSlice, slice, getExcel, index }) {
  const viz_type = slice.form_data.viz_type;
  let isTitle = true;
  let isImportExcel = true;
  const theRequest = GetRequest();
  let isManager = true;
  let isFilter = false;
  if(theRequest.hasOwnProperty("isManager")){
    isManager = theRequest.isManager === 'true' ? true : false;
  }

  if (viz_type === 'filter_box' || viz_type === 'big_number_viz' || viz_type === 'big_number_two_viz' || viz_type === 'big_number_three_viz' || viz_type === 'markup' || viz_type === 'filter_box_combination' || viz_type === 'filter_box_tree' || viz_type === 'big_number_four_viz') {
    isTitle = false;
  }

  if (viz_type === 'markup' || viz_type === 'separator'|| viz_type === 'filter_box_combination'){
    isImportExcel = false;
  }

  if (viz_type === 'filter_box' || viz_type === 'filter_box_combination' || viz_type === 'filter_box_tree') {
    isFilter = true;
  }

  let icon = '';
  MenuType.forEach(function (element) {
    if (element.chart === viz_type) {
      icon = element.icon.toString();
    }
  }, this);
  const classNum = index % 6;

  //set filter_combination slices div
  let filterSlicesDiv = null;
  if(slice.form_data.viz_type === 'filter_box_combination') {
    filterSlicesDiv = 
    slice.form_data.filter_combination.map(sliceId => (
      // <div id={"con_" + sliceId} style={{float: 'left', marginTop: 20}}></div>
      <div id={"con_" + sliceId} style={{float: 'left'}}></div>
    ));
  }
  // console.info(filterSlicesDiv)

  return (
    <div className="slice-cell" id={`${slice.slice_id}-cell`}
      style={{ marginTop: (isFilter) ? '-21px' : '0px', marginBottom: (isFilter) ? '-21px' : '0px' }}>
      {isTitle &&
        <div className="chart-header">
          <div className="row">
            <div className={`col-md-12 header header-${classNum}`}>
              <span className={icon} ></span>
              <span className="slice-title">{slice.nick_name}</span>&nbsp;
              {slice.subtitleAble &&
                <span className="slice-subtitle">{slice.subtitle}</span>
              }
            </div>
            <div className="col-md-12 chart-controls" style={{ paddingTop: 12 }}>
              <div className="pull-right">
                {(slice.description && isManager) &&
                  <a title={t('Toggle chart description')}>
                    <i
                      className="fa fa-info-circle slice_info"
                      title={slice.description}
                      data-toggle="tooltip"
                    />
                  </a>
                }

                <div className="btn-group" >
                  <a className="btn green btn-circle btn-sm hand-btn hand-btn-circle hand-btn-default"
                    data-toggle="dropdown"
                    data-hover="dropdown"
                    data-close-others="false"
                    aria-expanded="false">
                    <i className="fa fa-wrench"></i>
                  </a>
                  <ul className="dropdown-menu pull-right" style={{ minWidth: 100, marginLeft: 5 }} id={"name"}>
                    {isManager &&
                      <li>
                        <a
                          href={slice.edit_url} target="_blank"
                          data-toggle="tooltip" style={{ padding: '3px 7px', }}
                        >
                          <i className="icon-pencil" >{t('Edit Slice')}</i>
                        </a>
                      </li>
                    }
                    {isManager &&
                      <li>
                        <a href={slice.slice_url} target="_blank"
                          data-toggle="tooltip" style={{ padding: '3px 7px', }}>
                          <i className="icon-share-alt" >{t('Navigate to Slice')}</i>
                        </a>
                      </li>
                    }
                    {isManager &&
                      <li>
                        <a
                          className="remove-chart"
                          data-toggle="tooltip" style={{ padding: '3px 7px', }}
                          onClick={() => { removeSlice(slice.slice_id); }}
                        >
                          <i className="icon-trash" >
                            {t('Remove Slice')}
                            </i>
                        </a>
                      </li>
                    }

                    {true && isImportExcel && slice.form_data !== undefined &&
                      <li>
                        <a data-toggle="tooltip" onClick={() => { getExcel(slice); }}
                          style={{ padding: '3px 7px', }}
                        >
                          <i className="icon-cloud-download">
                            {t('Export to excel')}
                          </i>
                        </a>
                      </li>
                    }

                  </ul>
                  <a title={t('Refresh Data')} className="refresh" data-toggle="tooltip">
                    <i className="icon-refresh  hand-btn hand-btn-circle hand-btn-default" />
                  </a>
                  {isManager &&
                    <a title={t('Move Slice')} data-toggle="tooltip" >
                      <i className="icon-cursor-move drag hand-btn hand-btn-circle hand-btn-default" />
                    </a>
                  }

                </div>
              </div>
            </div>
          </div>
        </div>
      }
      <div
        className="slice_description bs-callout bs-callout-default"
        style={
          expandedSlices &&
            expandedSlices[String(slice.slice_id)] ? {} : { display: 'none' }
        }
        dangerouslySetInnerHTML={{ __html: slice.description_markeddown }}
      />
      <div className="row chart-container">
        <input type="hidden" value="false" />
        <div id={'token_' + slice.slice_id} className="token col-md-12">
          <img
            src="/static/assets/images/loading.gif"
            className="loading"
            alt="loading"
          />
          {!isTitle && isManager &&
            //<div className="pull-right chart-controls" style={{ top: '-15px', paddingBottom: '0px', marginBottom: '-20px' }}>
            <div className="pull-right chart-controls" style={(isFilter) ?
              { position: 'fixed', height: '5px', top: '0px', paddingBottom: '0px', marginBottom: '-20px' } :
              { top: '-15px', paddingBottom: '0px', marginBottom: '-20px' }}>
              <div className="btn-group" style={{ float: 'right' }}>
                  <a className="btn green btn-circle btn-sm hand-btn hand-btn-circle hand-btn-default"
                    data-toggle="dropdown"
                    data-hover="dropdown"
                    data-close-others="false"
                    aria-expanded="false" 
                    style={{marginRight: '5px'}}>
                    <i className="fa fa-wrench"></i>
                  </a>
                  <ul className="dropdown-menu pull-right" style={{ minWidth: 100, marginLeft: 5 }} id={"name"}>
                    {isManager &&
                      <li>
                        <a
                          href={slice.edit_url} target="_blank"
                          data-toggle="tooltip" style={{ padding: '3px 7px', }}
                        >
                          <i className="icon-pencil" >{t('Edit Slice')}</i>
                        </a>
                      </li>
                    }
                    {isManager &&
                      <li>
                        <a href={slice.slice_url} target="_blank"
                          data-toggle="tooltip" style={{ padding: '3px 7px', }}>
                          <i className="icon-share-alt" >{t('Navigate to Slice')}</i>
                        </a>
                      </li>
                    }
                    {isManager &&
                      <li>
                        <a
                          className="remove-chart"
                          data-toggle="tooltip" style={{ padding: '3px 7px', }}
                          onClick={() => { removeSlice(slice.slice_id); }}
                        >
                          <i className="icon-trash" >
                            {t('Remove Slice')}
                            </i>
                        </a>
                      </li>
                    }

                    {true && isImportExcel && slice.form_data !== undefined &&
                      <li>
                        <a data-toggle="tooltip" onClick={() => { getExcel(slice); }}
                          style={{ padding: '3px 7px', }}
                        >
                          <i className="icon-cloud-download">
                            {t('Export to excel')}
                          </i>
                        </a>
                      </li>
                    }

                  </ul>
                  <a title={t('Refresh Data')} className="refresh" data-toggle="tooltip" style={{marginRight: '5px'}}>
                    <i className="icon-refresh  hand-btn hand-btn-circle hand-btn-default" />
                  </a>
                  {isManager &&
                    <a title={t('Move Slice')} data-toggle="tooltip" >
                      <i className="icon-cursor-move drag hand-btn hand-btn-circle hand-btn-default" />
                    </a>
                  }
              </div>
            </div>
          }
          {filterSlicesDiv}
          {!isTitle &&
            <div className={`slice_container ${slice.form_data.viz_type}`} id={'con_' + slice.slice_id}>
            </div>
          }
          {isTitle &&
            //<div className={`slice_container`} id={'con_' + slice.slice_id} style={{ paddingLeft: 20, paddingRight: 20, paddingTop: 10, paddingBottom: 10 }} >
            <div className={`slice_container`} id={'con_' + slice.slice_id} style={{
              paddingLeft: (slice.form_data.viz_type === 'china_city_map' || slice.form_data.viz_type === 'echarts_china_city_map_migration') ? 0 : 20,
              paddingRight: (slice.form_data.viz_type === 'china_city_map' || slice.form_data.viz_type === 'echarts_china_city_map_migration') ? 0 : 20,
              paddingTop: (slice.form_data.viz_type === 'china_city_map' || slice.form_data.viz_type === 'echarts_china_city_map_migration') ? 0 : 10,
              paddingBottom: 10
            }} >
            </div>
          }
        </div>
      </div>
    </div>
  );
}

SliceCell.propTypes = propTypes;

export default SliceCell;
