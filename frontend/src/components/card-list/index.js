import styles from './style.module.css'


const CardList = ({ children }) => {
  return <div className={styles.cardList}>
    {children}
  </div>
}

export default CardList