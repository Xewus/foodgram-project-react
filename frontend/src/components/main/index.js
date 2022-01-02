import React from 'react'
import styles from './style.module.css'

const Main = ({ children }) => {
  return <main className={styles.main}>
    {children}
  </main>
}

export default Main
