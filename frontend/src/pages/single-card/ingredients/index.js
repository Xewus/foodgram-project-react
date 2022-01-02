import styles from './styles.module.css'

const Ingredients = ({ ingredients }) => {
  if (!ingredients) { return null }
  return <div className={styles.ingredients}>
    <h3 className={styles['ingredients__title']}>Ингридиенты:</h3>
    <div className={styles['ingredients__list']}>
      {ingredients.map(({
        name,
        amount,
        measurement_unit
      }) => <p
        key={`${name}${amount}${measurement_unit}`}
        className={styles['ingredients__list-item']}
      >
        {name} - {amount} {measurement_unit}
      </p>)}
    </div>
  </div>
}

export default Ingredients

