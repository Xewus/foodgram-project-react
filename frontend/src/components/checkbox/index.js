import cn from 'classnames'
import styles from './styles.module.css'
import { useState } from 'react'
import { Icons } from '../index'
import { hexToRgba } from '../../utils'

const Checkbox = ({
  onChange,
  className,
  color,
  value = false,
  name,
  id
}) => {
  const clickHandler = () => {
    onChange && onChange(id)
  }
  const classNames = cn(styles.checkbox, className, {
    [styles['checkbox_active']]: value
  })

  return <div className={styles['checkbox-container']}>
    <button
      className={classNames}
      onClick={clickHandler}
      style={{ backgroundColor: value && color }}
      type='button'
    >
      {value ? <Icons.CheckIcon /> : ''}
    </button>
    <span>{name}</span>
  </div>
}


export default Checkbox