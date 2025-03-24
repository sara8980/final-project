import React, { FC, useState, useEffect } from 'react';
import './UploadPicture.scss';
import { upload } from '@testing-library/user-event/dist/upload';
import axios from 'axios';
import { useUploadFile } from "dex-react-file-upload";
import { FileUploader } from "react-drag-drop-files";
import { Container, Row, Col } from 'react-bootstrap';
import { Button } from 'react-bootstrap';
import fileService from '../../services/file.service';
import Nav from '../navbar/navbar'
import AgesTree from '../Ages-tree/Ages-tree';
import Logo from '../Logo/Logo';
const fileTypes = ["JPG", "PNG", "GIF"];
interface YourImageProps { }

const YourImage: FC<YourImageProps> = () => {
  const [file, setFile] = useState<any>(null);
  const [isDisplay, setIsDisplay] = useState(false)
  const handleChange = (file: any) => {
    setFile(file);
  }

  const handleDragOver = (event: any) => {
    event.preventDefault()
  }

  const handleButtonClick = () => {
    setIsDisplay(true)


  };


  return (
    <div className='YourImage'>
      <Nav />
      {isDisplay ? ' ' : <Container>
        <div className="text-center mt-5">
          <h3>Upload or drag your image</h3>
        </div>
        <Row className=" row item-center text-center">
          <Col sm={6} className="mt-5 m-auto">
            {/* הגרירה של הקבצים */}
            <FileUploader className='col-sm-12'
              style={{ width: '100%' }}
              handleChange={handleChange}
              name="file"
              types={fileTypes}
            />
          </Col>
        </Row>
        {!file ? (
          <Logo></Logo>
        ) : (
          ""
        )}
        {/* התמונה */}
        {file &&
          <div className="ImageContainer items-center mt-5">
            <img
              src={URL.createObjectURL(file)}
              alt="Uploaded Preview" style={{
                maxWidth: '100%',
                height: 'auto',
                maxHeight: '50vh',
                objectFit: 'contain'
              }}
            />
          </div>
        }

        {/* כפתור שליחה */}
        {file && <Button
          className="col-sm-6 mt-5 mx-auto d-block"
          variant="success"
          size="lg"
          onClick={handleButtonClick}
        >
          Send
        </Button>}


      </Container>}
      {isDisplay ? <AgesTree file={file}></AgesTree> : ''}
    </div>

  );
};
export default YourImage;
