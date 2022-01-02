import { useState, useEffect, useRef } from 'react'
import styles from './styles.module.css'
import { Button } from '../index'
import cn from 'classnames'

const FileInput = ({ label, onChange, file = null, className }) => {
  const [ currentFile, setCurrentFile ] = useState(file)
  const fileInput = useRef(null)
  useEffect(_ => {
    if (file !== currentFile) {
      setCurrentFile(file)
    }
  }, [file])

  const getBase64 = (file) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function () {
      setCurrentFile(reader.result)
      onChange(reader.result)
    };
    reader.onerror = function (error) {
      console.log('Error: ', error);
    }
  }

  return <div className={cn(styles.container, className)}>
    <label className={styles.label}>
      {label}
    </label>
    <input
      className={styles.fileInput}
      type='file'
      ref={fileInput}
      onChange={e => {
        const file = e.target.files[0]
        getBase64(file)
      }}
    />
    <div
      onClick={_ => {
        fileInput.current.click()
      }}
      className={styles.button}
      type='button'
    >
      Выбрать файл
    </div>
    {currentFile && <div className={styles.image} style={{
      backgroundImage: `url(${currentFile})`
    }} />}
  </div>
}

export default FileInput