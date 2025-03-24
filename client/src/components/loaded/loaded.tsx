import React, { FC } from 'react';
import './loaded.scss';

interface LoadedProps {
  title: string
}
const Loaded: FC<LoadedProps> = (props: LoadedProps) => (
  <div className=" row  d-flex align-items-center   m-5">
    <div className="col-sm-12 ">
      <div className=" spinner-border m-5" role="status" aria-hidden="true"></div>
      <br></br>
      <strong>{props.title}</strong>
    </div>
  </div>
);

export default Loaded;
