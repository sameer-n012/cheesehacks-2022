export default function UploadForm() {

    return (
        <div>
            <h2>This is the upload page!</h2>
            <form method="POST" action="/api/upload" enctype="multipart/form-data">
                <input name="class_code" placeholder="Class code: "/>
                <input type="file" name="file" />
                <input type="submit" value="Upload" />
            </form>
        </div>
    )

}