import React, { FC, useEffect, useState } from 'react';
import './Ages-tree.scss';

import fileService from '../../services/file.service';
import Loadder from '../loaded/loaded'
import Nav from '../navbar/navbar'
import Avatar from '@mui/joy/Avatar';



interface AgesTreeProps {
  file: any
}

const AgesTree: FC<AgesTreeProps> = (props: AgesTreeProps) => {
  const [listApi, setList] = useState<any[]>()
  const [listHash] = useState<any>({});
  const [isDisplay, setIsDisplay] = useState<any>(false)
  const [errorMessage, setErrorMessage] = useState<any>('')
  const ageGroups = [
    "elderly", "adult", "young", "teenager", "child", "baby"
  ];
  const sortTheList = (data: [string, any][]) => {


    data.forEach((a) => {
      //בודקים אם אין קבוצה של גיל כאת
      if (!listHash[a[1]]) {
        //יוצרים קבוצה של גילאים ל אנשים
        listHash[a[1]] = [];
      }
      //דוחפים את הנתון-הלקוח לגיל המתאים
      listHash[a[1]].push(a);
    })

  }

  useEffect(() => {
    loadItems();
  }, [])

  const loadItems = () => {

    setIsDisplay(true);
    fileService.UploadFile(props.file)
      .then(res => {
        if (res.data != "error") {
          setErrorMessage('')
          console.log(res.data);
          setList(res.data);
          sortTheList(res.data);
          console.log(listHash);

          setIsDisplay(false);
        } else {


          setIsDisplay(false);
           setErrorMessage('No faces found! please upload another picture')
          console.error('Empty data received from server');

        }
      })
      .catch(error => {
        console.error('Error uploading file:', error);
        // Handle error if needed
      });



  }


  return (
    <div>
      <div className="ages-tree">
        {isDisplay && (
          <div className="loadder-container">
            <Loadder title='loadd data by axios' />
          </div>
        )}
        {errorMessage != '' && (
          <div className="alert alert-danger" role="alert">
            {errorMessage}
          </div>
        )}

        <div className={isDisplay ? 'hidden-content' : ''}></div>
        {Object.keys(listHash).map((group: any) => (
          <div className="group row" key={group}>
            <h3>{ageGroups[group]}</h3>
            {listHash[group].map((a: any, i: any) => (
              <div className="item" key={i}>
                <Avatar src={`data:image/jpeg;base64,${a[0]}`} size='lg' style={{ transform: 'scale(3)' }} />
              </div>
            ))}
          </div>
        ))}



      </div>
    </div>
  );

};

export default AgesTree;

