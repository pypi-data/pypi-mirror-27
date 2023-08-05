import React from 'react';
import { render } from 'react-dom';

import List from './component/List';

const $ = window.$ = require('jquery');
const jQuery = window.jQuery = $; // eslint-disable-line

const appContainer = document.getElementById('app');
const model = appContainer.getAttribute('model');
const params = {};
params['_oc_' + model] = 'modified';
params['_od_' + model] = 'desc';
render(
    <List
      model={model}
      params={params}
    />,
    appContainer
  );
