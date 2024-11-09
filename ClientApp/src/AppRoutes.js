import { Counter } from "./components/Counter";
import { FetchData } from "./components/FetchData";
import  Home  from "./components/Home";
import Maps from "./components/Maps";

const AppRoutes = [
  {
    index: true,
    element: <Home />
  },
  {
    path: '/maps',
    element: <Maps />
  },
  {
    path: '/fetch-data',
    element: <FetchData />
  }
];

export default AppRoutes;
