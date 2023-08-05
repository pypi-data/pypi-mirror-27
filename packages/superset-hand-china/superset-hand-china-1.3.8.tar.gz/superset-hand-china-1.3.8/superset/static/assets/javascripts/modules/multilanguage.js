

export function query(formData, queryResponse) {
  const vizT = ['ag_grid','echarts_bar', 'echarts_bar_waterfall', 'echarts_bar_h', 'echarts_area_stack',
    'echarts_line_bar', 'echarts_line', 'echarts_pie_m', 'echarts_pie_h', 'echarts_pie_g',
    'echarts_multiple_ring_diagram', 'echarts_dash_board', 'echarts_big_number_compare', 'echarts_treemap',
    'echarts_big_number', 'big_number_viz', 'echarts_radar_map', 'echarts_pie_h_g', 'table'
    , 'echarts_bar_progress','echarts_bubble','china_city_map','echarts_china_map','echarts_china_city_map_migration'
    ,'echarts_quadrant']
  // 返回的数据用data.d获取内容
  if (vizT.indexOf(formData.viz_type) != -1) {
    const data = queryResponse
    let keys = Object.keys(formData)
    keys.forEach(function (key, index) {
      if (key.indexOf('groupby') >= 0) {
          let group = []
            for (let mf in formData[key]) {
              for (let dg in data.groupby) {
                if (formData[key][mf] == data.groupby[dg][0]) {
                  group.push(data.groupby[dg][1])
                }
              }
            }
            if (group.length != 0) {
              formData[key] = group
            }
      }
      //table
      if(key == 'granularity_sqla'){
        if(formData.viz_type == 'table'){
          let gs = ''
          for(let m in data.groupby){
            if(formData[key] == data.groupby[m][0])
              gs = data.groupby[m][1]
          }
          if(gs != '')
            formData[key]= gs
        }        
      }
      if(key == 'all_columns'){
        if(formData.viz_type == 'table'){
          let all = []
          for(let i in formData[key] ){
            for(let m in data.groupby){
              if(formData[key][i] == data.groupby[m][0]){
                all.push(data.groupby[m][1])
              }
            }
          }
          if(all.length != 0){
            formData.all_columns =all
          }
        }
      }
      if( key == 'order_by_cols'){
        if(formData.viz_type == 'table'){
          let obcol = []
          let gm = data.groupby.concat(data.metrics)
          console.info(gm)
          for(let i in formData[key]){
            if(typeof(formData[key][i]) == 'string'){
            const fk = formData[key][i].substring(1,formData[key][i].length-1).split(',')
            console.info(fk[0])
            console.info(fk[0].substring(1,fk[0].length-1))
            for(let g in gm){
              if(fk[0].substring(1,fk[0].length-1) == gm[g][0]){
                let ob=""
                ob = '["'+ gm[g][1]+'",'+fk[1]+']'
                obcol.push(ob)
              }
            }
          }
        }
        
        if(obcol.length != 0){
          formData.order_by_cols = obcol
        }
      }
         
     
      }
      //zhexianzhuzhuangtu
      if (key == 'line_choice') {
        if (formData[key] != ('' || null)) {
          let choice = []
          for (let mf in formData[key]) {
            for (let dm in data.metrics) {
              if (formData[key][mf] == data.metrics[dm][0]) {
                choice.push(data.metrics[dm][1])
              }
            }
          }
          if (choice.length != 0) {
            formData.line_choice = choice
          }
        }
      }
      //echarts bubble
      if (key == 'size') {
        if (formData[key] != ('' || null)) {
          let ci = ''
          for (let mf in formData[key]) {
            for (let dm in data.metrics) {
              if (formData[key] == data.metrics[dm][0]) {
                ci = data.metrics[dm][1]
              }
            }
          }
          if (ci != '') {
            formData.size = ci
          }
        }
      }
      if (key == 'series') {
        if (formData[key] != ('' || null)) {
          let ci = ''
          for (let mf in formData[key]) {
            for (let dm in data.groupby) {
              if (formData[key] == data.groupby[dm][0]) {
                ci = data.groupby[dm][1]
              }
            }
          }
          if (ci != '') {
            formData.series = ci
          }
        }
      }
      if (key == 'entity') {
        if (formData[key] != ('' || null)) {
          let ci = ''
          for (let mf in formData[key]) {
            for (let dm in data.groupby) {
              if (formData[key] == data.groupby[dm][0]) {
                ci = data.groupby[dm][1]
              }
            }
          }
          if (ci != '') {
            formData.entity = ci
          }
        }
      }
      if (key == 'x') {
        if (formData[key] != ('' || null)) {
          let ci = ''
          for (let mf in formData[key]) {
            for (let dm in data.metrics) {
              if (formData[key] == data.metrics[dm][0]) {
                ci = data.metrics[dm][1]
              }
            }
          }
          if (ci != '') {
            formData.x = ci
          }
        }
      }
      if (key == 'y') {
        if (formData[key] != ('' || null)) {
          let ci = ''
          for (let mf in formData[key]) {
            for (let dm in data.metrics) {
              if (formData[key] == data.metrics[dm][0]) {
                ci = data.metrics[dm][1]
              }
            }
          }
          if (ci != '') {
            formData.y = ci
          }
        }
      }
      //map
      if(key == 'groupby_one'){
        if(typeof (formData[key]) == 'string'){
          let ci = ''
          for(let dm in data.groupby){
            if(formData[key] == data.groupby[dm][0])
            ci = data.groupby[dm][1]
          }
          if( ci != ''){
            formData.groupby_one = ci
          }
        }
      }
      //treemap
      if (key == 'child_id') {
        if (formData[key] != ('' || null)) {
          let ci = ''
          for (let mf in formData[key]) {
            for (let dm in data.groupby) {
              if (formData[key] == data.groupby[dm][0]) {
                ci = data.groupby[dm][1]
              }
            }
          }
          if (ci != '') {
            formData.child_id = ci
          }
        }
      }
      if (key == 'child_name') {
        if (formData[key] != ('' || null)) {
          let cn = ''
          for (let mf in formData[key]) {
            for (let dm in data.groupby) {
              if (formData[key] == data.groupby[dm][0]) {
                cn = data.groupby[dm][1]
              }
            }
          }
          if (cn != '') {
            formData.child_name = cn
          }
        }
      }
      if (key == 'parent_id') {
        if (formData[key] != ('' || null)) {
          let pi = ''
          for (let mf in formData[key]) {
            for (let dm in data.groupby) {
              if (formData[key] == data.groupby[dm][0]) {
                pi = data.groupby[dm][1]
              }
            }
          }
          if (pi != '') {
            formData.parent_id = pi
          }
        }
      }
      if (key == 'columns') {
        if (formData[key].length >0) {
          let imo = []
          for (let mf in formData[key]) {
            for (let dm in data.metrics) {
              if (formData[key] == data.metrics[dm][0]) {
                imo.push(data.metrics[dm][1])
              }
            }
          }
          if (imo != '') {
            formData.columns = imo
          }
        }
      }      
      //echarts_p_h
      if (key == 'inner_metrics_one') {
        if (formData[key] != ('' || null)) {
          let imo = ''
          for (let mf in formData[key]) {
            for (let dm in data.groupby) {
              if (formData[key] == data.groupby[dm][0]) {
                imo = data.groupby[dm][1]
              }
            }
          }
          if (imo != '') {
            formData.inner_metrics_one = imo
          }
        }
      }
      if (key == 'outer_metrics_one') {
        if (formData[key] != ('' || null)) {
          let imo = ''
          for (let mf in formData[key]) {
            for (let dm in data.groupby) {
              if (formData[key] == data.groupby[dm][0]) {
                imo = data.groupby[dm][1]
              }
            }
          }
          if (imo != '') {
            formData.outer_metrics_one = imo
          }
        }
      }
      if (key.indexOf('metric') >= 0) {
        if (formData[key] != ('' || null)) {
          if (typeof (formData[key]) == 'object') {
            let metric = []
            for (let mf in formData[key]) {
              for (let dm in data.metrics) {
                if (formData[key][mf] == data.metrics[dm][0]) {
                  metric.push(data.metrics[dm][1])
                }
                if (formData[key][mf] == data.metrics[dm][1]) {
                  if(formData.viz_type == 'echarts_china_map')
                  metric.push(data.metrics[dm][1])
                }
              }
            }

            if (metric.length != 0) {
              formData[key] = metric
               if(formData.viz_type == 'echarts_china_map'){
                  formData[key] = metric.unique3()
               }
            }

          }
          if (typeof (formData[key]) == 'string') {
            let metric = ''
            for (let dm in data.metrics) {
              if (formData[key] == data.metrics[dm][0]) {
                metric = data.metrics[dm][1]
              }
            }
            if (metric != '') {
              formData[key] = metric
            }
          }
        }
      }
    });
    return formData
  }
  else {
    return formData
  }
}
Array.prototype.unique3 = function(){
 var res = [];
 var json = {};
 for(var i = 0; i < this.length; i++){
  if(!json[this[i]]){
   res.push(this[i]);
   json[this[i]] = 1;
  }
 }
 return res;
}