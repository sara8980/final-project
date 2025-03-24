import React, { FC } from 'react';
import './NotFound.scss';

interface NotFoundProps {}

const NotFound: FC<NotFoundProps> = () => {
  return (
    <div className="not-found row col-sm-12">
      
      <h1>404 - הדף לא נמצא</h1>
      <p>אנו מצטערים, אך הדף שחיפשת אינו נמצא.</p>
      <p>אנא נסה שוב מאוחר יותר או חזור ל<a href="/">דף הבית</a>.</p>
    </div>
  );
};

export default NotFound;
