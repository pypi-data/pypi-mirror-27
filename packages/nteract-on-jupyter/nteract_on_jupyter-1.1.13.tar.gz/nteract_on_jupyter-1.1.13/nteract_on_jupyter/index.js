// @flow
import React from "react";
import ReactDOM from "react-dom";

import { Provider } from "react-redux";

import NotificationSystem from "react-notification-system";

import configureStore from "./store";
import Contents from "./providers/contents";

type JupyterConfigData = {
  token: string,
  page: "tree" | "view" | "edit",
  contentsPath: string,
  baseUrl: string,
  appVersion: string
};

import { NotebookApp } from "@nteract/core/providers";

function createApp(jupyterConfigData: JupyterConfigData) {
  const store = configureStore({ config: jupyterConfigData });
  window.store = store;

  class App extends React.Component<*> {
    notificationSystem: NotificationSystem;

    componentDidMount(): void {
      store.dispatch({ type: "LOAD", path: jupyterConfigData.contentsPath });
    }

    render(): React$Element<any> {
      return (
        <Provider store={store}>
          <div>
            {/* <Contents /> */}
            <NotebookApp />
            <NotificationSystem
              ref={notificationSystem => {
                this.notificationSystem = notificationSystem;
              }}
            />
          </div>
        </Provider>
      );
    }
  }

  return App;
}

function main(rootEl: Element, dataEl: Node | null) {
  // When the data element isn't there, provide an error message
  // Primarily for development usage
  const ErrorPage = (props: { error?: Error }) => (
    <div>
      <h1>ERROR</h1>
      <pre>Unable to parse / process the jupyter config data.</pre>
      {props.error ? props.error.message : null}
    </div>
  );

  if (!dataEl) {
    ReactDOM.render(<ErrorPage />, rootEl);
    return;
  }

  let jupyterConfigData: JupyterConfigData;

  try {
    jupyterConfigData = JSON.parse(dataEl.textContent);
  } catch (err) {
    ReactDOM.render(<ErrorPage error={err} />, rootEl);
    return;
  }

  const App = createApp(jupyterConfigData);
  ReactDOM.render(<App />, rootEl);
}

const rootEl = document.querySelector("#root");
const dataEl = document.querySelector("#jupyter-config-data");

// $FlowFixMe: querySelector can return null so this freaks out.
main(rootEl, dataEl);
