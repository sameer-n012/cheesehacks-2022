import { Container } from 'react-bootstrap'
import Header from '../components/Header'

export default function NotFound() {

    return (
        <div>
            <Header page='student_home'/>
            <Container className='p-4'>     
                <Container className='d-flex p-5 align-items-center justify-content-center' style={{marginTop: '10rem'}}>
                    <p className='fs-4 mt-4'>Sorry, this page does not exist</p>
                </Container>    
            </Container>
        </div>
    )

}