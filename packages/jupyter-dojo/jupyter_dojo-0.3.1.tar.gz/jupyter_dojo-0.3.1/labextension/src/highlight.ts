import {
  NotebookPanel
} from '@jupyterlab/notebook';

import {
  CodeCell
} from '@jupyterlab/cells';


import {
  Mode
} from '@jupyterlab/codemirror';


interface HashMapOfMimes {
  [key: string]: string;
}

export
function register_highlight(panel: NotebookPanel) {
  // ToDo: erase mime
  let activeCell = panel.notebook.activeCell;
  let original: HashMapOfMimes = {};
  let callback = () => {
    if (activeCell instanceof CodeCell) {
      let split = activeCell.model.value.text.split(" ");
      if (split && split.length > 2 && split[0] == "%%write") {
        //activeCell.model.mimeType = split[1];
        if (!(activeCell.id in original)) {
          original[activeCell.id] = activeCell.model.mimeType;
        }
        activeCell.model.mimeType = Mode.findByName(split[1]).mime;
      } else {
        if (activeCell.id in original) {
          //activeCell.model.mimeType = panel.notebook.codeMimetype;
          activeCell.model.mimeType = original[activeCell.id];
          delete original[activeCell.id];
        }
      }
    }
  };
  if (activeCell) {
    activeCell.model.value.changed.connect(callback);
  }
  panel.notebook.activeCellChanged.connect((notebook, cellview) => {
    if (activeCell) {
      activeCell.model.value.changed.disconnect(callback);
    }
    activeCell = panel.notebook.activeCell;
    if (activeCell) {
      activeCell.model.value.changed.connect(callback);
    }
  });
}