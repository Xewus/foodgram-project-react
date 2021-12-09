import cn from 'classnames'
import styles from './style.module.css'

const Button = ({
  children,
  modifier = 'style_light-blue',
  href,
  clickHandler,
  className,
  disabled,
  type = 'button'
}) => {
  const classNames = cn(styles.button, className, {
    [styles[`button_${modifier}`]]: modifier,
    [styles.button_disabled]: disabled
  })
  if (href) {
    return <a
      className={classNames}
      href={href}
    >
      {children}
    </a>
  }
  return <button
    className={classNames}
    disabled={disabled}
    onClick={_ => clickHandler && clickHandler()}
  >
    {children}
  </button>
}


export default Button