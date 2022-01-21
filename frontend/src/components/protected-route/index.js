import React from 'react';
import { Route, Redirect } from "react-router-dom";

function ProtectedRoute({ exact, component: Component, path, ...props }) {
  return (
    <Route path={path} exact={exact}>
      {
        () => props.loggedIn ? <Component {...props} /> : <Redirect to='/signin' />
      } 
    </Route>
  )
}
export default ProtectedRoute;