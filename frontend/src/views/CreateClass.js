export default function CreateClass() {

    return (
        <div>
            <h2>Create your class here</h2>
            <form method="POST" action="/api/create-class" enctype="multipart/form-data">
                <input name="class_code" placeholder="Class code: "/>
                <input type="submit" value="Upload" />
            </form>
        </div>
    )

}