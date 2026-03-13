import {BrowserRouter, Routes, Navigate,  Route} from "react-router-dom";

function App() {

  return (
    <BrowserRouter>
    <Routes>
      <Route index element={ <Navigate to={"/dashboard"} />} />
      <Route path="/dashboard"/>
      <Route path="/runs" />
      <Route path="/review-queue" />
    </Routes>
    </BrowserRouter>
  )
}

export default App
