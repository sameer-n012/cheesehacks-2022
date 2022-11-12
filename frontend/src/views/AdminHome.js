import Header from '../components/Header'
import { useEffect, useState } from 'react'
import { Container, Accordion, Col, Row, Button} from 'react-bootstrap'

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

			<Container className=''>
                <Accordion alwaysOpen>
                    {sampleClasses.map((c) => (
                        <Accordion.Item eventKey={c.joincode}>
                            <Accordion.Header className=''>{c.name}</Accordion.Header>
                            <Accordion.Body>
								<Container className='d-flex'>
									<Container className='d-flex flex-column p-2 align-items-center justify-content-center'>
										<Container className='d-flex w-50'>
											<p>Join Code: {c.joincode}</p>
											<Button type="button" class="btn btn-outline-danger">Copy</Button>
										</Container>
										<Container className='d-flex w-50 p-2 align-items-center justify-content-center'>
											<p>Today's Attendance: {c.attendance.length + '/' + c.classSize}</p>
											<Button type="button" class="btn btn-outline-danger">Export to CSV</Button>
										</Container>
									
									</Container>
									<Container className='d-flex align-items-center justify-content-center'>
										<Button type="button" class="btn btn-outline-danger">Launch Button</Button>
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
