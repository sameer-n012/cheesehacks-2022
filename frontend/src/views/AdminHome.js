import clipboardy from 'clipboardy';
import Header from '../components/Header'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Container, Accordion, Button} from 'react-bootstrap'

async function copyFunction(joincode) {
	await clipboardy.write(joincode);
	const text = await clipboardy.read();
	console.log(text); // 'butter'
}



export default function AdminHome() {

    const navigate = useNavigate();
    
    const currentUser = localStorage.getItem('current_userid')
    console.log(currentUser)

    const [classes, setClasses] = useState([])

    useEffect(() => { //TODO flask fetch
        
        const requestOptions = {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        };

        let response = -1
        fetch('/api/get-classes?userid=' + currentUser, requestOptions).then(
            response => response.json() 
        ).then(
            data => setClasses(data)
        );

        console.log('fetching classes')
        console.log(classes)
    }, [currentUser]);

	// const sampleClasses = [
    //     {
    //         name: 'c1',
    //         joincode: 'aj09iu231je',
	// 		attendance: ['s1', 's2'],
    //         classSize: 150
    //     },
    //     {
    //         name: 'c2',
    //         joincode: 'jeoij2e19je',
	// 		attendance: ['s1', 's2'],
    //         classSize: 150
    //     },
    //     {
    //         name: 'c3',
    //         joincode: 'cxmzf98201',
	// 		attendance: ['s1', 's2'],
    //         classSize: 150
    //     }
    // ];

    const exportToCSV = () => {
        // TODO get attendance

        const requestOptions = {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        };

        let response = -1
        fetch('/api/get-attendance', requestOptions).then(
            response => response.status 
        ).then(
            status => { response = status; }
        );

        const rows = [
            ["", "d1", "d2", "d3", "d4", "d5", "d6"],
            ["s1", "x", "o", "x", "x", "x", "o"],
            ["s2", "x", "x", "x", "o", "x", "x"]
        ];
        
        let csvContent = "data:text/csv;charset=utf-8," 
            + rows.map(e => e.join(",")).join("\n");
    
        var encodedUri = encodeURI(csvContent);
        var link = document.createElement("a");
        link.setAttribute("href", encodedUri);

        let dateStr = new Date().toISOString().slice(0,10).replace(/-/g, "");

        link.setAttribute("download", "attendance_" + dateStr + ".csv");
        document.body.appendChild(link); // Required for FF
        
        link.click();
    }

	return (
		
		<div className='teacherhome'>
            <Header  page='teacher_home'/>

			<Container className='p-4 align-items-center justify-content-center'>
                <Accordion alwaysOpen>
                    {classes.map((c) => (
                        <Accordion.Item eventKey={c.code} key={c.code}>
                            <Accordion.Header className=''>{c.name}</Accordion.Header>
                            <Accordion.Body>
                                <Container className='d-flex flex-row p-2 align-items-center justify-content-center'>
                                    <Container className='d-flex p-2 flex-column align-items-center justify-content-around'>
                                        <p>Join Code: {c.code}</p>
                                        <Button variant='outline-dark' onClick={() => {navigate('/detect')}}> Launch Detection </Button>
                                    </Container>
                                    <Container className='d-flex p-2 flex-column align-items-center justify-content-around'>
                                        <p>Today's Attendance: {c.num_present + '/' + c.class_size}</p>
                                        <Button  variant="outline-dark" onClick={exportToCSV}>Export to CSV</Button>
                                    </Container>
                                </Container>
                            </Accordion.Body>
                        </Accordion.Item>
                    ))}
                </Accordion>
			</Container>
				
			
		</div>
	);
}
