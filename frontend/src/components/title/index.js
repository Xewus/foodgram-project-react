import styles from './styles.module.css'
import cn from 'classnames'

const Title = ({ title, className }) => {
  return <h1 className={cn(styles.title, className)}>
    {title}
  </h1>
}

export default Title