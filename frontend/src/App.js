import logo from './logo.svg';
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './views/Home';
import NotFound from './views/NotFound';
import StudentHome from './views/StudentHome';
import StudentUpload from './views/StudentUpload';
import AdminHome from './views/AdminHome';
import FaceDetection from './views/FaceDetection';

function App() {

	return (
        <BrowserRouter>
            <Routes>
                <Route path='/' element={<Home />} />
                <Route path='/student' element={<StudentHome />} />
                <Route path='/upload' element={<StudentUpload />} />
                <Route path='/admin' element={<AdminHome />} />
                <Route path='/detect' element={<FaceDetection />} />
                {/* Add other routes here */}
                <Route path='*' element={<NotFound />} />
            </Routes>
        </BrowserRouter>
	);
}

export default App;
