import styles from './styles.module.css'
import cn from 'classnames'
import { Icons, Button, LinkComponent } from '../index'
const countForm = (number, titles) => {
  number = Math.abs(number);
  if (Number.isInteger(number)) {
    let cases = [2, 0, 1, 1, 1, 2];  
    return titles[ (number % 100 > 4 && number % 100 < 20) ? 2 : cases[(number%10<5)?number%10:5] ]
  }
  return titles[1];
}

const Subscription = ({ email, first_name, last_name, username, removeSubscription, recipes_count, id, recipes }) => {
  const shouldShowButton = recipes_count  > 3
  const moreRecipes = recipes_count - 3
  return <div className={styles.subscription}>
    <div className={styles.subscriptionHeader}>
      <h2 className={styles.subscriptionTitle}>
        <LinkComponent className={styles.subscriptionRecipeLink} href={`/user/${id}`} title={`${first_name} ${last_name}`} />
      </h2>
    </div>
    <div className={styles.subscriptionBody}>
      <ul className={styles.subscriptionItems}>
        {recipes.map(recipe => {
          return <li className={styles.subscriptionItem} key={recipe.id}>
            <LinkComponent className={styles.subscriptionRecipeLink} href={`/recipes/${recipe.id}`} title={
              <div className={styles.subscriptionRecipe}>
                <img src={recipe.image} alt={recipe.name} className={styles.subscriptionRecipeImage} />
                <h3 className={styles.subscriptionRecipeTitle}>
                  {recipe.name}
                </h3>
                <p className={styles.subscriptionRecipeText}>
                  <Icons.ClockIcon />{recipe.cooking_time} мин.
                </p>
              </div>
            } />
          </li>
        })}
        {shouldShowButton && <li className={styles.subscriptionMore}>
          <LinkComponent
            className={styles.subscriptionLink}
            title={`Еще ${moreRecipes} ${countForm(moreRecipes, ['рецепт', 'рецепта', 'рецептов'])}...`}
            href={`/user/${id}`}
          />
        </li>}
      </ul>
    </div>
    <div className={styles.subscriptionFooter}>
      <Button
        className={styles.subscriptionButton}
        clickHandler={_ => {
          removeSubscription({ id })
        }}
      >
        Отписаться
      </Button>
    </div>
  </div>
}

export default Subscription
