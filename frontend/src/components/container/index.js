import styles from './style.module.css'
import cn from 'classnames'

const Container = ({ children, className }) => {
  return <div className={cn(styles.container, className)}>
    {children}
  </div>
}

export default Container