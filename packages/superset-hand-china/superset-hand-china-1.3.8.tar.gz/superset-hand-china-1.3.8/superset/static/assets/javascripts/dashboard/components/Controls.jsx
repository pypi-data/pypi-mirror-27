import React from 'react';
import PropTypes from 'prop-types';
import { ButtonGroup } from 'react-bootstrap';

import Button from '../../components/Button';
import CssEditor from './CssEditor';
import RefreshIntervalModal from './RefreshIntervalModal';
import SaveModal from './SaveModal';
import CodeModal from './CodeModal';
import SliceAdder from './SliceAdder';
import { t } from '../../locales';
import domtoimage from 'dom-to-image';

const $ = window.$ = require('jquery');

const propTypes = {
  dashboard: PropTypes.object.isRequired,
};

class Controls extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      css: props.dashboard.css || '',
      theme: props.dashboard.theme,
      refreshAble: props.dashboard.refreshAble,
      cssTemplates: [],
    };
  }
  componentWillMount() {
    $.get('/csstemplateasyncmodelview/api/read', (data) => {
      const cssTemplates = data.result.map(row => ({
        value: row.template_name,
        css: row.css,
        label: row.template_name,
      }));
      this.setState({ cssTemplates });
    });
  }
  refresh() {
    // Force refresh all slices
    this.props.dashboard.renderSlices(this.props.dashboard.sliceObjects, true);
  }


  svgToCanvas(svgElem, dashboardTitle, typeString) {
    let j = 0;
    const _this = this;
    svgElem.each(function (index, node) {
      svgAsDataUri(node, {}, function (uri) {
        let parentNode = node.parentNode;
        let canvas = document.createElement('canvas');

        let img = new Image();
        img.src = uri;

        img.onload = function () {
          canvas.width = img.width;
          canvas.height = img.height;

          let context = canvas.getContext('2d');  //取得画布的2d绘图上下文  
          context.drawImage(img, 0, 0);

          if (node.style.position) {
            canvas.style.position += node.style.position;
            canvas.style.left += node.style.left;
            canvas.style.top += node.style.top;
          }
          parentNode.removeChild(node);
          parentNode.appendChild(canvas);
          j++;
          if (j === svgElem.length) {
            if (typeString === 'png') {
              _this.canvasToPNG(dashboardTitle);
            } else if (typeString === 'pdf') {
              _this.canvasToPDF(dashboardTitle);
            }
          }
        }
      });
    });
  }

  tablesSvgToCanvas(dataTables, svgElem, dashboardTitle, typeString) {
    let i = 0;
    const _this = this;
    dataTables.each(function (index, node) {
      domtoimage.toPng(node)
        .then(function (dataUrl) {
          let parentNode = node.parentNode;
          let canvas = document.createElement('canvas');
          let img = new Image();
          img.src = dataUrl;

          img.onload = function () {
            canvas.width = img.width;
            canvas.height = img.height;

            let context = canvas.getContext('2d');  //取得画布的2d绘图上下文  
            context.drawImage(img, 0, 0);

            if (node.style.position) {
              canvas.style.position += node.style.position;
              canvas.style.left += node.style.left;
              canvas.style.top += node.style.top;
            }
            parentNode.removeChild(node);
            parentNode.appendChild(canvas);
            i++;
            if (i === dataTables.length) {
              if (svgElem === null && typeString === 'png') {
                _this.canvasToPNG(dashboardTitle);
              } else if (svgElem === null && typeString === 'pdf') {
                _this.canvasToPDF(dashboardTitle);
              } else {
                _this.svgToCanvas(svgElem, dashboardTitle, typeString);
              }
            }
          }
        })
        .catch(function (error) {
          console.error('oops, something went wrong!', error);
        });
    });
  }

  canvasToPNG(dashboardTitle) {
    html2canvas($("#grid-container"), {
      onrendered: function (canvas) {
        let imgUri = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream"); // 获取生成的图片的url  
        let save_link = document.createElementNS('http://www.w3.org/1999/xhtml', 'a');
        save_link.href = imgUri;
        save_link.download = dashboardTitle + '.png';
        let event = new MouseEvent("click", {
          bubbles: true,
          cancelable: true,
          view: window,
        });
        //var event = document.createEvent('MouseEvents');
        //event.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
        save_link.dispatchEvent(event);
      },
      background: "#fff",
      allowTaint: true
    });
  }

  canvasToPDF(dashboardTitle) {
    html2canvas($("#grid-container"), {
      onrendered: function (canvas) {
        let contentWidth = canvas.width;
        let contentHeight = canvas.height;
        let docDefinition = {
          pageSize: {width:contentWidth+50, height:contentHeight+50},
          content: [
            {
              image: canvas.toDataURL('image/png', 1.0),
            }]
        }
        pdfMake.createPdf(docDefinition).download(dashboardTitle + '.pdf');
      },
      background: "#fff",
      allowTaint: true
    });
  }

  domToPNGOrPDF(dataTables, svgElem, dashboardTitle, typeString) {
    if (dataTables.length > 0 && svgElem.length === 0) {
      this.tablesSvgToCanvas(dataTables, null, dashboardTitle, typeString);
    } else if (dataTables.length === 0 && svgElem.length > 0) {
      this.svgToCanvas(svgElem, dashboardTitle, typeString);
    } else if (dataTables.length > 0 && svgElem.length > 0) {
      this.tablesSvgToCanvas(dataTables, svgElem, dashboardTitle, typeString);
    } else {
      if (typeString === 'png') {
        this.canvasToPNG(dashboardTitle);
      } else if (typeString === 'pdf') {
        this.canvasToPDF(dashboardTitle);
      }
    }
  }

  calHeatmapToCanvas(typeString) {
    let dashboardTitle = this.props.dashboard.dashboard_title;
    if (dashboardTitle === null || dashboardTitle === '' || $.trim(dashboardTitle).length === 0) {
      let date = new Date();
      dashboardTitle = 1900 + date.getYear() + '-' + (1 + date.getMonth()) + '-' + date.getDate() + '-' + date.getHours() + '-' + date.getMinutes() + '-' + date.getSeconds();
    }
    let calHeatmap = $(".cal-heatmap-container");
    if (calHeatmap.length > 0) {
      let k = 0;
      const _this = this;
      calHeatmap.each(function (index, node) {
        svgAsDataUri(node, {}, function (uri) {
          let parentNode = node.parentNode;
          let canvas = document.createElement('canvas');

          let img = new Image();
          img.src = uri;

          img.onload = function () {
            canvas.width = img.width;
            canvas.height = img.height;

            let context = canvas.getContext('2d');  //取得画布的2d绘图上下文  
            context.drawImage(img, 0, 0);

            if (node.style.position) {
              canvas.style.position += node.style.position;
              canvas.style.left += node.style.left;
              canvas.style.top += node.style.top;
            }
            parentNode.removeChild(node);
            parentNode.appendChild(canvas);
            k++;
            if (k === calHeatmap.length) {
              let dataTables = $(".dataTables_wrapper");
              let svgElem = $("#grid-container").find('svg');//divReport为需要截取成图片的dom的id
              _this.domToPNGOrPDF(dataTables, svgElem, dashboardTitle, typeString);
            }
          }
        });
      });
    } else {
      let dataTables = $(".dataTables_wrapper");
      let svgElem = $("#grid-container").find('svg');//divReport为需要截取成图片的dom的id
      this.domToPNGOrPDF(dataTables, svgElem, dashboardTitle, typeString);
    }
  }

  downloadImage() {
    this.calHeatmapToCanvas('png');
  }

  downloadPDF() {
    this.calHeatmapToCanvas('pdf');
  }

  changeCss(css) {
    this.setState({ css });
    this.props.dashboard.onChange();
  }
  changeTheme(theme) {
    this.setState({ theme });
    this.props.dashboard.onChange();
  }
  changeRefresh(refreshAble) {
    this.setState({ refreshAble });
    this.props.dashboard.onChange();
  }
  change(opt, type) {
    if (type === 'css') {
      this.changeCss(opt);
    } else if (type === 'theme') {
      this.changeTheme(opt);
    } else if (type === 'refresh') {
      this.changeRefresh(opt);
    }
  }

  getQueryString(name) {
    const reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    const r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]);
    return null;
  }

  render() {
    const dashboard = this.props.dashboard;
    const emailBody = t('Checkout this dashboard: %s', window.location.href);
    const emailLink = 'mailto:?Subject=Superset%20Dashboard%20'
      + `${dashboard.dashboard_title}&Body=${emailBody}`;
    return (
      <ButtonGroup>
        <Button
          tooltip={t('Force refresh the whole dashboard')}
          onClick={this.refresh.bind(this)}
        >
          <i className="fa fa-refresh" />
        </Button>
        <SliceAdder
          dashboard={dashboard}
          triggerNode={
            <i className="fa fa-plus" />
          }
        />
        <RefreshIntervalModal
          onChange={refreshInterval => dashboard.startPeriodicRender(refreshInterval * 1000)}
          triggerNode={
            <i className="fa fa-clock-o" />
          }
        />
        <Button
          tooltip={t('download dashboard to png')}
          onClick={this.downloadImage.bind(this)}
        >
          <i className="fa fa-file-image-o" />
        </Button>
        <Button
          tooltip={t('download dashboard to pdf')}
          onClick={this.downloadPDF.bind(this)}
        >
          <i className="fa fa-file-pdf-o" />
        </Button>
        <CodeModal
          codeCallback={dashboard.readFilters.bind(dashboard)}
          triggerNode={<i className="fa fa-filter" />}
        />
        <CssEditor
          dashboard={dashboard}
          triggerNode={
            <i className="fa fa-css3" />
          }
          initialCss={dashboard.css}
          templates={this.state.cssTemplates}
          onChange={this.change.bind(this)}
          theme={dashboard.theme}
          themes={dashboard.themes}
          sliceResizeAble={dashboard.sliceResizeAble}
          refreshAble={dashboard.refreshAble}
        />
        <Button
          onClick={() => { window.location = emailLink; }}
        >
          <i className="fa fa-envelope" />
        </Button>
        <Button
          disabled={!dashboard.dash_edit_perm}
          onClick={() => {
            window.location = `/dashboardmodelview/edit/${dashboard.id}`;
          }}
          tooltip={t('Edit this dashboard\'s properties')}
        >
          <i className="fa fa-edit" />
        </Button>
        <SaveModal
          dashboard={dashboard}
          css={this.state.css}
          theme={this.state.theme}
          refreshAble={this.state.refreshAble}
          triggerNode={
            <Button disabled={!dashboard.dash_save_perm}>
              <i className="fa fa-save" />
            </Button>
          }
        />
      </ButtonGroup>
    );
  }
}
Controls.propTypes = propTypes;

export default Controls;
