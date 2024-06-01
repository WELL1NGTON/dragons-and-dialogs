import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
} from "react-router-dom";
import Home from "./Pages/Home";
import About from "./Pages/About";

const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route path="/about" element={<About />} />
      <Route path="/" element={<Home />} />
    </>
  )
);

export default function AppRouter() {
  return <RouterProvider router={router} />;
}
