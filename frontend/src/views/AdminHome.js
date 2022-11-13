import clipboardy from 'clipboardy';
import Header from '../components/Header'
import { useEffect, useState } from 'react'
import { Container, Accordion, Button} from 'react-bootstrap'

async function copyFunction(joincode) {
	await clipboardy.write(joincode);
	const text = await clipboardy.read();
	console.log(text); // 'butter'
}

function exportToCSV(){

}

export default function AdminHome() {

	const sampleClasses = [
        {
            name: 'c1',
            joincode: 'aj09iu231je',
			attendance: ['s1', 's2'],
            classSize: 150
        },
        {
            name: 'c2',
            joincode: 'jeoij2e19je',
			attendance: ['s1', 's2'],
            classSize: 150
        },
        {
            name: 'c3',
            joincode: 'cxmzf98201',
			attendance: ['s1', 's2'],
            classSize: 150
        }
    ];


	

	return (

		
		<div className='teacherhome'>
            <Header  page='teacher_home'/>

		
			<ul>

			<Container className='p-4 align-items-center justify-content-center'>
                <Accordion alwaysOpen>
                    {sampleClasses.map((c) => (
                        <Accordion.Item eventKey={c.joincode}>
                            <Accordion.Header className=''>{c.name}</Accordion.Header>
                            <Accordion.Body>
								<Container className='d-flex'>
									<Container className='d-flex flex-column p-2 align-items-center justify-content-center'>
										<Container className='d-flex w-50'>
											<p>Join Code: {c.joincode}</p>
											<button class="btn btn-outline-danger" onClick={copyFunction(c.joincode)} >Copy</button>
										</Container>
										<Container className='d-flex w-50 p-2 align-items-center justify-content-center'>
											<p>Today's Attendance: {c.attendance.length + '/' + c.classSize}</p>
											<button  class="btn btn-outline-danger">Export to CSV</button>
										</Container>
									
									</Container>
									<Container className='d-flex align-items-center justify-content-center'>
										<a href="/detect" class="btn btn-outline-danger btn-lg" role="button"> Launch Button </a>
									</Container>
								</Container>
                            </Accordion.Body>
                        </Accordion.Item>
                    ))}
                </Accordion>
			</Container>
				
			</ul>
		</div>
	);
}
