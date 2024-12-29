import { Admin, Resource, ShowGuesser } from "react-admin";
import { Layout } from "./Layout";
import fastApiProvider from "./fastApiProvider";
import { TaskList } from "./TaskList";

export const App = () => (
  <Admin layout={Layout} dataProvider={fastApiProvider}>
    <Resource name="tasks" list={TaskList} show={ShowGuesser} />
  </Admin>
);
