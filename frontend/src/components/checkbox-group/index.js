import cn from 'classnames'
import styles from './styles.module.css'
import { useState } from 'react'
import { Checkbox } from '../index'

const CheckboxGroup = ({
  onUpdated,
  label,
  values = [],
  handleChange,
  className,
  labelClassName,
  tagsClassName,
  checkboxClassName
}) => {
  return <div className={cn(styles.checkboxGroup, className)}>
    {label && <div className={cn(styles.label, labelClassName)}>
      {label}
    </div>}
    <div className={cn(styles.checkboxGroupItems, tagsClassName)}>
      {values.map(item => {
        return <Checkbox
          key={item.id}
          id={item.id}
          value={item.value}
          name={item.name}
          color={item.color}
          onChange={handleChange}
          className={checkboxClassName}
        />
      })}
    </div>
  </div>
}


export default CheckboxGroup