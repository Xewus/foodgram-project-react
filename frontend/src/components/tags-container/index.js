import styles from './styles.module.css'
import cn from 'classnames'
import { Tag } from '../index'

const TagsContainer = ({ tags }) => {
  if (!tags) { return null }
  return <div className={styles['tags-container']}>
    {tags.map(tag => {
      return <Tag
        key={tag.id}
        color={tag.color}
        name={tag.name}
      />
    })}
  </div>
}

export default TagsContainer
