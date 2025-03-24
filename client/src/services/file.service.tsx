import axios from'axios'
export default new class FileService {
    
    BASE_URL="https://jsonplaceholder.typicode.com/users";
   
    getListApi(){
        return axios.get(`${this.BASE_URL}`);
    }

    inserNewApi(api:any){
        return axios.post(`${this.BASE_URL}/entries`,api)
    }

    deleteApi(apiId:number){
        return axios.delete(`${this.BASE_URL}/entries/${apiId}`)
    }


    UploadFile(file:any,url:string=''){
        //העברת רשימת קבצים לשרת
        //עי יצירת אובייקט FormData -js object
        let formFile=new FormData();
       console.log(file)
            //העצסת רשימת הקבצים לתוך "המשאית"
            formFile.append("file",file)
           
       
        return axios.post("http://127.0.0.1:5000/image",formFile,{
            headers:{
                "Content-Type":"multipart/form-data"
            }
        })     
      
    }
    getList(){return axios.get("http://127.0.0.1:5000/image");

    }

}