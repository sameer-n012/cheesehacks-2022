import logo from './logo.svg';
import './App.css';
import {BrowserRouter, Routes, Route} from 'react-router-dom'
import Home from './views/Home';
import NotFound from './views/NotFound';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />}/>
        {/* Add other routes here */}
        <Route path="*" element={<NotFound />} />
      </Routes>
  </BrowserRouter>
  );
}

export default App;
