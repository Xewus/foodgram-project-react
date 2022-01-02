import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import styles from './styles.module.css'
import cn from 'classnames'

const Textarea = ({
    onChange,
    placeholder,
    label,
    disabled,
    textareaClassName,
    labelClassName,
    value
  }) => {

  const [ inputValue, setInputValue ] = useState(value)
  const handleValueChange = (e) => {
    const value = e.target.value
    setInputValue(value)
    onChange(e)
  }

  useEffect(_ => {
    if (value !== inputValue) {
      setInputValue(value)
    }
  }, [value])

  return <div className={styles.textarea}>
    <label className={cn(styles.textareaLabel, labelClassName)}>
      <div className={styles.textareaLabelText}>
        {label}
      </div>
      <textarea
        rows="8"
        value={inputValue}
        className={cn(styles.textareaField, textareaClassName)}
        onChange={e => {
          handleValueChange(e)
        }}
      />
    </label>
  </div>
}

export default Textarea
