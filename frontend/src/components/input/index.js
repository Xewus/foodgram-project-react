import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import styles from './styles.module.css'
import cn from 'classnames'

const Input = ({
    onChange,
    placeholder,
    label,
    disabled,
    type = 'text',
    inputClassName,
    labelClassName,
    className,
    name,
    required,
    onFocus,
    onBlur,
    value = ''
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


  return <div className={cn(styles.input, className)}>
    <label className={styles.inputLabel}>
      {label && <div className={cn(styles.inputLabelText, labelClassName)}>
        {label}
      </div>}
      <input
        type={type}
        required={required}
        name={name}
        className={cn(styles.inputField, inputClassName)}
        onChange={e => {
          handleValueChange(e)
        }}
        onFocus={onFocus}
        value={inputValue}
        onBlur={onBlur}
      />
    </label>
  </div>
}

export default Input
