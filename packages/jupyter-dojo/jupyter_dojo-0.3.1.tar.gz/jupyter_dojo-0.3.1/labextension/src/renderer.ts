import {
  Widget
} from '@phosphor/widgets';

import {
  NotebookPanel
} from '@jupyterlab/notebook';

import {
  IRenderMime
} from '@jupyterlab/rendermime-interfaces';


import {
  DojoView, TestStatus
} from '@jupyter_dojo/base';


export
class RenderedData extends Widget implements IRenderMime.IRenderer {

  view: DojoView;

  constructor(options: IRenderMime.IRendererOptions, view: DojoView) {
    super();
    this._load_mimetype = options.mimeType;
    this.view = view;
  }

  renderModel(model: IRenderMime.IMimeModel): Promise<void> {
    let data = model.data[this._load_mimetype] as string;
    let value: TestStatus = JSON.parse(JSON.stringify(data));
    this.view.renderResult(value);
    return Promise.resolve();
  }

  private _load_mimetype: string;
}

export
function register_renderer(panel: NotebookPanel, dojoView: DojoView): void {
  const rendererFactory: IRenderMime.IRendererFactory = {
    safe: true,
    mimeTypes: ['application/unittest.status+json'],
    createRenderer: options => new RenderedData(options, dojoView)
  };

  panel.notebook.rendermime.addFactory(rendererFactory, 0);

}