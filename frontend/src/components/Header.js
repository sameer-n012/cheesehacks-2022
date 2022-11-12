export default function Header({page}) {

    // TODO insert application name
	return (
		<div className='header' backgroundColor='#990000'>
			<h2 className='header-title' color='#ffffff'>Face Attendance</h2>
            {page == 'student_home' ? (
                <div>
                    <button className='header-button'>Join Class</button>
                    <button className='header-button'>Upload Image</button>
                </div>
            ) : page == 'teacher_home' ? (
                <div>
                    <button className='header-button'>Create Class</button>
                </div>
            ) : (
                <div>
                    
                </div>
            )}
		</div>
	);
}
