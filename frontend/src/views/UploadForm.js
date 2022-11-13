import '../App.css'
import Form from 'react-bootstrap/Form';
import { Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

export default function UploadForm() {
    const navigate = useNavigate();


    return (
        <div>
            <form method="POST" action="/api/upload" enctype="multipart/form-data">
                <div className="d-flex flex-column align-items-center">
                    
                    <Form.Group controlId="formFileLg" className="mb-3">
                        <Form.Control type="file" name="file" size="lg" />
                    </Form.Group>
                    
                    <input type="submit" value="Upload" className="btn btn-outline-dark w-25 m-3"/>
                    <button onClick={()=>{navigate('/student')}} className="btn btn-outline-dark w-25 m-3">Back</button>
                </div>
            </form>
        </div>
    )

}