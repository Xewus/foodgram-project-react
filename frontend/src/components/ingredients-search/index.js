import styles from './styles.module.css'

const IngredientsSearch = ({ ingredients, onClick }) => {
  return <div className={styles.container}>
    {ingredients.map(({ name, id, measurement_unit }) => {
      return <div key={id} onClick={_ => onClick({ id, name, measurement_unit })}>{name}</div>
    })}
  </div>
}

export default IngredientsSearch